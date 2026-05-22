"""
数据下载脚本 - 数据分析个人作业 P01
姓名：廖婉琼  学号：25210178
"""
import os
import sys
import time
import datetime
import pandas as pd
import numpy as np
import akshare as ak
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STOCK_DIR = os.path.join(DATA_DIR, 'stock')
INDEX_DIR = os.path.join(DATA_DIR, 'index')
MACRO_DIR = os.path.join(DATA_DIR, 'macro')
FINANCE_DIR = os.path.join(DATA_DIR, 'finance')
LOG_FILE = os.path.join(BASE_DIR, 'download_log.txt')

START_DATE = '20200101'
END_DATE = datetime.datetime.now().strftime('%Y%m%d')

# 10只股票
stocks = [
    {'code': '002594', 'name': '比亚迪',   'industry': '汽车'},
    {'code': '601633', 'name': '长城汽车', 'industry': '汽车'},
    {'code': '600519', 'name': '贵州茅台', 'industry': '白酒'},
    {'code': '000858', 'name': '五粮液',   'industry': '白酒'},
    {'code': '601857', 'name': '中国石油', 'industry': '能源'},
    {'code': '601088', 'name': '中国神华', 'industry': '能源'},
    {'code': '600941', 'name': '中国移动', 'industry': '通讯'},
    {'code': '000063', 'name': '中兴通讯', 'industry': '通讯'},
    {'code': '002352', 'name': '顺丰控股', 'industry': '物流'},
    {'code': '600233', 'name': '圆通速递', 'industry': '物流'},
]

# ============================================================
# 下载日志
# ============================================================
def log_download(name, success, shape=None, error=None):
    timestamp = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    if success:
        msg = f'{timestamp} SUCCESS  {name}  shape={shape}'
    else:
        msg = f'{timestamp} FAILED   {name}  Error: {error}'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)
    return success

# 初始化日志
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write(f'# 数据下载日志 - 廖婉琼 25210178\n')
    f.write(f'# 开始时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write(f'# 数据范围: {START_DATE} ~ {END_DATE}\n')
    f.write('#' * 60 + '\n')

print(f'项目目录: {BASE_DIR}')
print(f'数据时间范围: {START_DATE} ~ {END_DATE}')
print()

# ============================================================
# 1. 下载个股后复权日度行情
# ============================================================
print('=' * 60)
print('1. 下载10只个股后复权日度行情')
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

        # 标准化列名
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

# ============================================================
# 2. 下载市场指数日度数据
# ============================================================
print('=' * 60)
print('2. 下载市场指数日度数据')
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

# ============================================================
# 3. 下载宏观经济指标（月度）
# ============================================================
print('=' * 60)
print('3. 下载宏观经济指标')
print('=' * 60)

# --- 3.1 CPI 同比增速（月度，年率数据） ---
print('\n3.1 CPI 同比增速...')
try:
    cpi_df = ak.macro_china_cpi_yearly()
    cpi_df['日期'] = pd.to_datetime(cpi_df['日期'])
    cpi_df = cpi_df[cpi_df['日期'] >= '2020-01-01'].copy()
    cpi_df = cpi_df.rename(columns={'日期': 'date', '今值': 'value'})
    cpi_df['indicator'] = 'CPI同比增速'
    cpi_df = cpi_df[['date', 'indicator', 'value']].dropna(subset=['value'])
    cpi_df.to_csv(os.path.join(MACRO_DIR, 'macro_cpi.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_cpi', True, shape=cpi_df.shape)
except Exception as e:
    log_download('macro_cpi', False, error=str(e))

# --- 3.2 人民币/美元汇率（央行中间价，月度聚合） ---
print('\n3.2 人民币/美元汇率...')
try:
    fx_df = ak.currency_boc_sina(symbol='美元')
    fx_df['日期'] = pd.to_datetime(fx_df['日期'])
    # 使用央行中间价
    fx_df = fx_df[['日期', '央行中间价']].copy()
    fx_df.columns = ['date', 'value']
    fx_df['date'] = pd.to_datetime(fx_df['date'])
    # 按月取最后一个交易日的汇率（月度）
    fx_df['month'] = fx_df['date'].dt.to_period('M')
    fx_monthly = fx_df.groupby('month').last().reset_index()
    fx_monthly['date'] = fx_monthly['month'].dt.to_timestamp()
    fx_monthly = fx_monthly[fx_monthly['date'] >= '2020-01-01'].copy()
    fx_monthly['indicator'] = 'USD_CNY汇率'
    fx_monthly = fx_monthly[['date', 'indicator', 'value']].dropna(subset=['value'])
    fx_monthly['value'] = pd.to_numeric(fx_monthly['value'], errors='coerce')
    # 汇率数据从2023年开始，补充说明
    fx_monthly.to_csv(os.path.join(MACRO_DIR, 'macro_usd_cny.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_usd_cny', True, shape=fx_monthly.shape)
    print(f'  注意: 汇率数据从 currency_boc_sina 获取，实际可用范围可能有限')
except Exception as e:
    log_download('macro_usd_cny', False, error=str(e))

# --- 3.3 M2 同比增速 ---
print('\n3.3 M2 同比增速...')
try:
    m2_df = ak.macro_china_money_supply()
    m2_df = m2_df.rename(columns={'月份': 'date'})
    # 处理日期格式（如 "2026年04月份"）
    m2_df['date'] = m2_df['date'].str.extract(r'(\d{4})\D+(\d{1,2})').apply(
        lambda x: f'{x[0]}-{int(x[1]):02d}-01', axis=1)
    m2_df['date'] = pd.to_datetime(m2_df['date'], errors='coerce')
    m2_df = m2_df[m2_df['date'] >= '2020-01-01'].copy()
    m2_df['value'] = pd.to_numeric(m2_df['货币和准货币(M2)-同比增长'], errors='coerce')
    m2_df['indicator'] = 'M2同比增速'
    m2_out = m2_df[['date', 'indicator', 'value']].dropna(subset=['value'])
    m2_out.to_csv(os.path.join(MACRO_DIR, 'macro_m2.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_m2', True, shape=m2_out.shape)
except Exception as e:
    log_download('macro_m2', False, error=str(e))

# --- 3.4 1年期LPR利率 ---
print('\n3.4 1年期LPR利率...')
try:
    lpr_df = ak.macro_china_lpr()
    lpr_df['TRADE_DATE'] = pd.to_datetime(lpr_df['TRADE_DATE'])
    lpr_df = lpr_df[lpr_df['TRADE_DATE'] >= '2020-01-01'].copy()
    lpr_df['date'] = lpr_df['TRADE_DATE']
    lpr_df['value'] = pd.to_numeric(lpr_df['LPR1Y'], errors='coerce')
    lpr_df['indicator'] = 'LPR1Y'
    lpr_out = lpr_df[['date', 'indicator', 'value']].dropna(subset=['value'])
    lpr_out.to_csv(os.path.join(MACRO_DIR, 'macro_lpr.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_lpr', True, shape=lpr_out.shape)
except Exception as e:
    log_download('macro_lpr', False, error=str(e))

# --- 3.5 工业增加值同比增速 ---
print('\n3.5 工业增加值同比增速...')
try:
    ind_df = ak.macro_china_industrial_production_yoy()
    ind_df['日期'] = pd.to_datetime(ind_df['日期'])
    ind_df = ind_df[ind_df['日期'] >= '2020-01-01'].copy()
    ind_df = ind_df.rename(columns={'日期': 'date', '今值': 'value'})
    ind_df['indicator'] = '工业增加值同比增速'
    ind_out = ind_df[['date', 'indicator', 'value']].dropna(subset=['value'])
    ind_out['value'] = pd.to_numeric(ind_out['value'], errors='coerce')
    ind_out.to_csv(os.path.join(MACRO_DIR, 'macro_industrial.csv'), index=False, encoding='utf-8-sig')
    log_download('macro_industrial', True, shape=ind_out.shape)
except Exception as e:
    log_download('macro_industrial', False, error=str(e))

print(f'\n宏观指标下载完成\n')

# ============================================================
# 4. 下载财务指标（长格式）
# ============================================================
print('=' * 60)
print('4. 下载财务指标（ROE、净利润率、资产负债率、营收增速）')
print('=' * 60)

finance_records = []
for s in stocks:
    print(f'\n  下载 {s["code"]} {s["name"]} 财务数据...')
    try:
        df = ak.stock_financial_abstract_ths(symbol=s['code'], indicator='按报告期')
        if df is None or df.empty:
            log_download(f'finance_{s["code"]}', False, error='No data')
            time.sleep(1)
            continue

        # 提取年度报告（12-31结尾）
        df['报告期'] = pd.to_datetime(df['报告期'], errors='coerce')
        df_annual = df[df['报告期'].dt.month == 12].copy()
        current_year = datetime.datetime.now().year
        df_annual = df_annual[df_annual['报告期'].dt.year >= current_year - 5]

        if df_annual.empty:
            log_download(f'finance_{s["code"]}', False, error='No annual data in last 5 years')
            time.sleep(1)
            continue

        # 提取需要的指标
        for _, row in df_annual.iterrows():
            year = row['报告期'].year

            # ROE
            try:
                roe = str(row.get('净资产收益率', ''))
                if roe and roe != 'False' and roe != '--':
                    roe_val = pd.to_numeric(roe.replace('%', ''), errors='coerce')
                    if not pd.isna(roe_val):
                        finance_records.append({
                            'code': s['code'], 'name': s['name'],
                            'year': year, 'indicator': 'ROE', 'value': roe_val
                        })
            except:
                pass

            # 净利润率
            try:
                npm = str(row.get('销售净利率', ''))
                if npm and npm != 'False' and npm != '--':
                    npm_val = pd.to_numeric(npm.replace('%', ''), errors='coerce')
                    if not pd.isna(npm_val):
                        finance_records.append({
                            'code': s['code'], 'name': s['name'],
                            'year': year, 'indicator': '净利润率', 'value': npm_val
                        })
            except:
                pass

            # 资产负债率
            try:
                alr = str(row.get('资产负债率', ''))
                if alr and alr != 'False' and alr != '--':
                    alr_val = pd.to_numeric(alr.replace('%', ''), errors='coerce')
                    if not pd.isna(alr_val):
                        finance_records.append({
                            'code': s['code'], 'name': s['name'],
                            'year': year, 'indicator': '资产负债率', 'value': alr_val
                        })
            except:
                pass

            # 营业收入增速
            try:
                revg = str(row.get('营业总收入同比增长率', ''))
                if revg and revg != 'False' and revg != '--':
                    revg_val = pd.to_numeric(revg.replace('%', ''), errors='coerce')
                    if not pd.isna(revg_val):
                        finance_records.append({
                            'code': s['code'], 'name': s['name'],
                            'year': year, 'indicator': '营业收入增速', 'value': revg_val
                        })
            except:
                pass

        n_records = len([r for r in finance_records if r['code'] == s['code']])
        log_download(f'finance_{s["code"]}_{s["name"]}', True, shape=(n_records, 5))
    except Exception as e:
        log_download(f'finance_{s["code"]}_{s["name"]}', False, error=str(e))

    time.sleep(1.5)

# 合并保存
if finance_records:
    finance_df = pd.DataFrame(finance_records)
    filepath = os.path.join(FINANCE_DIR, 'finance_ratios.csv')
    finance_df.to_csv(filepath, index=False, encoding='utf-8-sig')
    log_download('finance_ratios_all', True, shape=finance_df.shape)
    print(f'\n财务数据已保存: {filepath} ({finance_df.shape[0]} 条记录)')
    print(f'\n各股票财务记录数:')
    print(finance_df.groupby(['code', 'name']).size().to_string())
else:
    print('\n未获取到任何财务数据!')

# ============================================================
# 5. 下载汇总
# ============================================================
print('\n' + '=' * 60)
print('5. 下载汇总')
print('=' * 60)

sections = {
    'stock': STOCK_DIR,
    'index': INDEX_DIR,
    'macro': MACRO_DIR,
    'finance': FINANCE_DIR,
}

for name, d in sections.items():
    files = [f for f in os.listdir(d) if f.endswith('.csv')]
    print(f'\n{name.upper()}/ ({len(files)} 个文件):')
    for f in sorted(files):
        fpath = os.path.join(d, f)
        size_kb = os.path.getsize(fpath) / 1024
        try:
            tmp = pd.read_csv(fpath)
            print(f'  {f}: {tmp.shape[0]} 行 x {tmp.shape[1]} 列, {size_kb:.1f} KB')
        except:
            print(f'  {f}: {size_kb:.1f} KB')

print(f'\n日志文件: {LOG_FILE}')
with open(LOG_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    success_count = sum(1 for l in lines if 'SUCCESS' in l)
    failed_count = sum(1 for l in lines if 'FAILED' in l)
    print(f'  总计: {success_count} 成功, {failed_count} 失败')

print('\n数据下载全部完成!')
