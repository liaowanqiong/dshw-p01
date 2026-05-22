import pandas as pd
import numpy as np

df = pd.read_csv('data/clean/stock_close_wide.csv', parse_dates=['date'])
hs = df['沪深300']

print('沪深300列统计:')
print('总行数:', len(hs))
print('NaN个数:', hs.isna().sum())

valid_idx = hs.notna()
if valid_idx.any():
    first = df.loc[valid_idx.idxmax(), 'date']
    last = df.loc[valid_idx[::-1].idxmax(), 'date']
    print('首个非NaN日期:', first)
    print('最后非NaN日期:', last)

# 检查日期连续性
df_sorted = df.sort_values('date').reset_index(drop=True)
dates = pd.to_datetime(df_sorted['date'])
diff_days = dates.diff().dropna().dt.days
print('\n日期间隔(天)统计:')
print(diff_days.describe())

# 找间隔>5天的行（diff_days比df少一行，所以index要对齐）
gap_idx = diff_days[diff_days > 5].index
if len(gap_idx) > 0:
    print('\n长间隔(>5天)的行:')
    for i in gap_idx:
        gap = int(diff_days.loc[i])
        d = str(df_sorted.loc[i, 'date'])[:10]
        print('  行', i, ':', d, ', 间隔=', gap, '天')
else:
    print('\n无异常长间隔')

# 检查归一化结果
print('\n=== 归一化合理性检查 ===')
normalized = df['沪深300'] / df['沪深300'].iloc[0]
print('归一化第1天:', round(normalized.iloc[0], 4), '(应为1.0)')
print('归一化最大值:', round(normalized.max(), 4))
print('归一化最小值:', round(normalized.min(), 4))
print('归一化末值:', round(normalized.iloc[-1], 4))

# 检查index_300_clean.csv的close是否和wide一致
print('\n=== 与index_300_clean.csv 对比 ===')
df300 = pd.read_csv('data/clean/index_300_clean.csv', parse_dates=['date'])
wide_sub = df[['date','沪深300']].rename(columns={'沪深300':'wide'}).dropna()
idx_sub = df300[['date','close']].rename(columns={'close':'idx'}).dropna()
merged = pd.merge(wide_sub, idx_sub, on='date', how='inner')
merged['diff'] = merged['wide'] - merged['idx']
print('合并行数:', len(merged))
print('差异 min:', round(merged['diff'].min(), 6))
print('差异 max:', round(merged['diff'].max(), 6))
if merged['diff'].abs().max() < 0.01:
    print('数据一致')
else:
    print('数据不一致!')
