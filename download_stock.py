"""
下载个股和指数数据 - 绕过代理
"""
import os
import time
import datetime
import pandas as pd
import akshare as ak
import warnings
warnings.filterwarnings('ignore')

# 绕过代理
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STOCK_DIR = os.path.join(DATA_DIR, 'stock')
INDEX_DIR = os.path.join(DATA_DIR, 'index')
LOG_FILE = os.path.join(BASE_DIR, 'download_log.txt')

START_DATE = '20200101'
END_DATE = datetime.datetime.now().strftime('%Y%m%d')

stocks = [
    {'code': '002594', 'name': '比亚迪'},
    {'code': '601633', 'name': '长城汽车'},
    {'code': '600519', 'name': '贵州茅台'},
    {'code': '000858', 'name': '五粮液'},
    {'code': '601857', 'name': '中国石油'},
    {'code': '601088', 'name': '中国神华'},
    {'code': '600941', 'name': '中国移动'},
    {'code': '000063', 'name': '中兴通讯'},
    {'code': '002352', 'name': '顺丰控股'},
    {'code': '600233', 'name': '圆通速递'},
]

def log_download(name, success, shape=None, error=None):
    timestamp = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    if success:
        msg = f'{timestamp} SUCCESS  {name}  shape={shape}'
    else:
        msg = f'{timestamp} FAILED   {name}  Error: {error}'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)

# 下载个股
print('=' * 60)
print('下载个股后复权日度行情（绕过代理）')
print('=' * 60)

stock_count = 0
for s in stocks:
    try:
        df = ak.stock_zh_a_hist(
            symbol=s['code'], period='daily',
            start_date=START_DATE, end_date=END_DATE,
            adjust='hfq'
        )
        if df is None or df.empty:
            log_download(f'stock_{s["code"]}_{s["name"]}', False, error='No data returned')
            continue

        col_map = {'日期': 'date', '开盘': 'open', '收盘': 'close',
                   '最高': 'high', '最低': 'low', '成交量': 'volume', '成交额': 'amount'}
        df = df.rename(columns=col_map)
        keep_cols = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount']
        df = df[[c for c in keep_cols if c in df.columns]]
        df.insert(0, 'code', s['code'])
        df.insert(1, 'name', s['name'])

        filepath = os.path.join(STOCK_DIR, f'stock_{s["code"]}.csv')
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        log_download(f'stock_{s["code"]}_{s["name"]}', True, shape=df.shape)
        stock_count += 1
    except Exception as e:
        log_download(f'stock_{s["code"]}_{s["name"]}', False, error=str(e))
    time.sleep(1)

print(f'\n个股下载完成: {stock_count}/{len(stocks)} 只成功\n')

# 下载指数
print('=' * 60)
print('下载市场指数日度数据（绕过代理）')
print('=' * 60)

indices = [
    {'code': '000300', 'name': '沪深300'},
    {'code': '000001', 'name': '上证综指'},
]

index_count = 0
for idx in indices:
    try:
        df = ak.stock_zh_index_daily_em(symbol=f'sh{idx["code"]}')
        if df is None or df.empty:
            log_download(f'index_{idx["code"]}', False, error='No data returned')
            continue

        df.columns = [c.lower() for c in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        start_dt = pd.to_datetime(START_DATE)
        end_dt = pd.to_datetime(END_DATE)
        df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)].copy()

        if df.empty:
            log_download(f'index_{idx["code"]}', False, error='No data in date range')
            continue

        df.insert(0, 'code', idx['code'])
        df.insert(1, 'name', idx['name'])

        filepath = os.path.join(INDEX_DIR, f'index_{idx["code"]}.csv')
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        log_download(f'index_{idx["code"]}_{idx["name"]}', True, shape=df.shape)
        index_count += 1
    except Exception as e:
        log_download(f'index_{idx["code"]}', False, error=str(e))
    time.sleep(1)

print(f'\n指数下载完成: {index_count}/{len(indices)} 个成功\n')

# 汇率数据也需要补全（之前只有9个月）
print('=' * 60)
print('补充下载完整汇率数据')
print('=' * 60)
MACRO_DIR = os.path.join(DATA_DIR, 'macro')
try:
    fx_df = ak.currency_boc_sina(symbol='美元')
    fx_df['日期'] = pd.to_datetime(fx_df['日期'])
    fx_df = fx_df[['日期', '央行中间价']].copy()
    fx_df.columns = ['date', 'value']
    fx_df['month'] = fx_df['date'].dt.to_period('M')
    fx_monthly = fx_df.groupby('month').last().reset_index()
    fx_monthly['date'] = fx_monthly['month'].dt.to_timestamp()
    fx_monthly = fx_monthly[fx_monthly['date'] >= '2020-01-01'].copy()
    fx_monthly['indicator'] = 'USD_CNY汇率'
    fx_monthly = fx_monthly[['date', 'indicator', 'value']].dropna(subset=['value'])
    fx_monthly['value'] = pd.to_numeric(fx_monthly['value'], errors='coerce')
    fx_monthly.to_csv(os.path.join(MACRO_DIR, 'macro_usd_cny.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_usd_cny_full', True, shape=fx_monthly.shape)
    print(f'  日期范围: {fx_monthly["date"].min()} ~ {fx_monthly["date"].max()}')
except Exception as e:
    log_download('macro_usd_cny_full', False, error=str(e))

print('\n全部完成!')
