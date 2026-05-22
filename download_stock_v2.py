"""
尝试用 baostock 下载个股和指数数据（备用方案）
"""
import os
import sys
import time
import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 清除代理
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STOCK_DIR = os.path.join(DATA_DIR, 'stock')
INDEX_DIR = os.path.join(DATA_DIR, 'index')
LOG_FILE = os.path.join(BASE_DIR, 'download_log.txt')

START_DATE = '2020-01-01'
END_DATE = datetime.datetime.now().strftime('%Y-%m-%d')

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

# ============================================================
# 方案1: 先尝试 akshare（清除代理后）
# ============================================================
print('=' * 60)
print('方案1: 尝试 akshare (已清除代理环境变量)')
print('=' * 60)

try:
    import akshare as ak
    # 快速测试
    test_df = ak.stock_zh_a_hist(symbol='600519', period='daily',
                                  start_date='20260501', end_date='20260522', adjust='hfq')
    if test_df is not None and not test_df.empty:
        print(f'akshare 连接成功! 测试数据: {test_df.shape}')
        AKSHARE_OK = True
    else:
        print('akshare 返回空数据')
        AKSHARE_OK = False
except Exception as e:
    print(f'akshare 连接失败: {type(e).__name__}: {e}')
    AKSHARE_OK = False

# ============================================================
# 方案2: 使用 baostock
# ============================================================
BS_OK = False
if not AKSHARE_OK:
    print('\n' + '=' * 60)
    print('方案2: 尝试 baostock')
    print('=' * 60)
    try:
        import baostock as bs
        lg = bs.login()
        print(f'baostock login: {lg.error_msg}')
        if lg.error_code == '0':
            BS_OK = True
            # 测试
            rs = bs.query_history_k_data_plus('sh.600519',
                'date,open,high,low,close,volume,amount',
                start_date='2026-05-01', end_date='2026-05-22',
                frequency='d', adjustflag='2')  # 2=后复权
            data = []
            while rs.next():
                data.append(rs.get_row_data())
            test_df = pd.DataFrame(data, columns=rs.fields)
            print(f'baostock 测试: {test_df.shape}')
            if test_df.empty:
                BS_OK = False
            bs.logout()
        else:
            BS_OK = False
    except ImportError:
        print('baostock 未安装，尝试安装...')
        os.system(f'{sys.executable} -m pip install baostock -q')
        try:
            import baostock as bs
            lg = bs.login()
            if lg.error_code == '0':
                BS_OK = True
                bs.logout()
        except:
            BS_OK = False
    except Exception as e:
        print(f'baostock 失败: {e}')
        BS_OK = False

# ============================================================
# 下载个股数据
# ============================================================
print('\n' + '=' * 60)
print(f'使用 {"akshare" if AKSHARE_OK else "baostock"} 下载个股数据')
print('=' * 60)

if AKSHARE_OK:
    import akshare as ak
    stock_count = 0
    for s in stocks:
        try:
            df = ak.stock_zh_a_hist(
                symbol=s['code'], period='daily',
                start_date='20200101', end_date=datetime.datetime.now().strftime('%Y%m%d'),
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
    print(f'个股下载完成: {stock_count}/{len(stocks)} 只成功')

elif BS_OK:
    import baostock as bs
    lg = bs.login()
    stock_count = 0
    for s in stocks:
        try:
            # baostock 代码格式: sh.600519 / sz.002594
            if s['code'].startswith('6'):
                bs_code = f'sh.{s["code"]}'
            else:
                bs_code = f'sz.{s["code"]}'

            rs = bs.query_history_k_data_plus(bs_code,
                'date,open,high,low,close,volume,amount',
                start_date=START_DATE, end_date=END_DATE,
                frequency='d', adjustflag='2')  # 后复权

            data = []
            while rs.next():
                data.append(rs.get_row_data())
            df = pd.DataFrame(data, columns=rs.fields)

            if df.empty:
                log_download(f'stock_{s["code"]}_{s["name"]}', False, error='No data returned')
                continue

            # 标准化
            for c in ['open', 'high', 'low', 'close', 'volume', 'amount']:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors='coerce')

            df = df.rename(columns={'date': 'date'})
            df.insert(0, 'code', s['code'])
            df.insert(1, 'name', s['name'])

            filepath = os.path.join(STOCK_DIR, f'stock_{s["code"]}.csv')
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            log_download(f'stock_{s["code"]}_{s["name"]} (baostock)', True, shape=df.shape)
            stock_count += 1
        except Exception as e:
            log_download(f'stock_{s["code"]}_{s["name"]}', False, error=str(e))
        time.sleep(0.5)

    bs.logout()
    print(f'个股下载完成: {stock_count}/{len(stocks)} 只成功')
else:
    print('!!! akshare 和 baostock 均不可用，无法下载个股数据 !!!')
    print('请在本地电脑上运行 download_all.py（确保网络畅通无代理）')

# ============================================================
# 下载指数数据
# ============================================================
print('\n' + '=' * 60)
print(f'下载指数数据')
print('=' * 60)

indices = [
    {'bs_code': 'sh.000300', 'ak_code': '000300', 'name': '沪深300'},
    {'bs_code': 'sh.000001', 'ak_code': '000001', 'name': '上证综指'},
]

index_count = 0
for idx in indices:
    if AKSHARE_OK:
        try:
            df = ak.stock_zh_index_daily_em(symbol=f'sh{idx["ak_code"]}')
            if df is not None and not df.empty:
                df.columns = [c.lower() for c in df.columns]
                df['date'] = pd.to_datetime(df['date'])
                df = df[(df['date'] >= START_DATE) & (df['date'] <= END_DATE)].copy()
                df.insert(0, 'code', idx['ak_code'])
                df.insert(1, 'name', idx['name'])
                filepath = os.path.join(INDEX_DIR, f'index_{idx["ak_code"]}.csv')
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                log_download(f'index_{idx["ak_code"]}_{idx["name"]}', True, shape=df.shape)
                index_count += 1
                time.sleep(1)
                continue
        except:
            pass

    if BS_OK:
        try:
            import baostock as bs
            lg2 = bs.login()
            rs = bs.query_history_k_data_plus(idx['bs_code'],
                'date,open,high,low,close,volume,amount',
                start_date=START_DATE, end_date=END_DATE,
                frequency='d', adjustflag='3')  # 不复权
            data = []
            while rs.next():
                data.append(rs.get_row_data())
            df = pd.DataFrame(data, columns=rs.fields)
            bs.logout()

            if not df.empty:
                for c in ['open', 'high', 'low', 'close', 'volume', 'amount']:
                    if c in df.columns:
                        df[c] = pd.to_numeric(df[c], errors='coerce')
                df.insert(0, 'code', idx['ak_code'])
                df.insert(1, 'name', idx['name'])
                filepath = os.path.join(INDEX_DIR, f'index_{idx["ak_code"]}.csv')
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                log_download(f'index_{idx["ak_code"]}_{idx["name"]} (baostock)', True, shape=df.shape)
                index_count += 1
            time.sleep(0.5)
        except Exception as e:
            log_download(f'index_{idx["ak_code"]}', False, error=str(e))
    else:
        log_download(f'index_{idx["ak_code"]}', False, error='No available data source')

print(f'\n指数下载完成: {index_count}/{len(indices)} 个成功')

# 汇率补全
print('\n' + '=' * 60)
print('补充汇率数据')
print('=' * 60)
MACRO_DIR = os.path.join(DATA_DIR, 'macro')
try:
    import akshare as ak
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

# 最终统计
print('\n' + '=' * 60)
print('最终数据统计')
print('=' * 60)
for d_name, d_path in [('STOCK', STOCK_DIR), ('INDEX', INDEX_DIR), ('MACRO', MACRO_DIR), ('FINANCE', os.path.join(DATA_DIR, 'finance'))]:
    files = [f for f in os.listdir(d_path) if f.endswith('.csv')]
    print(f'\n{d_name}/ ({len(files)} 个文件):')
    for f in sorted(files):
        fp = os.path.join(d_path, f)
        sz = os.path.getsize(fp) / 1024
        try:
            tmp = pd.read_csv(fp)
            print(f'  {f}: {tmp.shape[0]} 行 x {tmp.shape[1]} 列, {sz:.1f} KB')
        except:
            print(f'  {f}: {sz:.1f} KB')

print('\n完成!')
