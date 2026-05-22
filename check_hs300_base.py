import pandas as pd

print('=== 1. stock_close_wide.csv ===')
df = pd.read_csv('data/clean/stock_close_wide.csv', parse_dates=['date'])
print('列名:', list(df.columns))
print('日期范围:', str(df['date'].min()), '~', str(df['date'].max()))
hs = df['沪深300'].dropna()
print('沪深300 非NaN行数:', len(hs))
print('沪深300 首行值:', round(hs.iloc[0], 2))
print('沪深300 末行值:', round(hs.iloc[-1], 2))
print('前5行 date + 沪深300:')
print(df[['date','沪深300']].head())

print('\n=== 2. index_300_clean.csv ===')
df2 = pd.read_csv('data/clean/index_300_clean.csv', parse_dates=['date'])
print('列名:', list(df2.columns))
print('日期范围:', str(df2['date'].min()), '~', str(df2['date'].max()))
print('前5行:')
print(df2.head())

print('\n=== 3. 归一化基准检查 ===')
day0 = df['date'].iloc[0]
val0 = df['沪深300'].iloc[0]
print('宽表第1行日期:', day0)
print('宽表第1行沪深300值:', round(val0, 2))
print('当前代码基准: iloc[0] (即数据的第1天)')
print('作业要求基准: 2020年第一个交易日 (=1)')

mask = df['date'] >= '2020-01-01'
if mask.any():
    idx = df.index[mask][0]
    d2020 = df.loc[idx, 'date']
    v2020 = df.loc[idx, '沪深300']
    print('\n2020年第一个交易日: 索引=' + str(idx) + ', 日期=' + str(d2020))
    print('当日沪深300值:', round(v2020, 2))
    if val0 > 0 and v2020 > 0:
        r = val0 / v2020
        print('-> 若以2020-01-02为基准，第1天归一化值 = ' + str(round(r, 4)) + ' (应为1)')
        if abs(r - 1.0) > 0.001:
            print('结论: 当前基准 != 2020年第一个交易日，需要修正!')
        else:
            print('结论: 当前基准就是2020年第一个交易日')
else:
    print('宽表中无2020年数据!')

print('\n=== 4. 宽表 vs index_300_clean 沪深300对比 ===')
a = df.set_index('date')[['沪深300']].rename(columns={'沪深300':'wide'})
b = df2.set_index('date')[['close']].rename(columns={'close':'idx'})
m = pd.concat([a, b], axis=1).dropna()
m['diff'] = m['wide'] - m['idx']
print('合并后行数:', len(m))
mn = round(m['diff'].min(), 6)
mx = round(m['diff'].max(), 6)
mean = round(m['diff'].mean(), 6)
print('价格差异: min=' + str(mn) + ', max=' + str(mx) + ', mean=' + str(mean))
if abs(mx) > 0.01 or abs(mn) > 0.01:
    print('⚠ 两个数据源价格不一致!')
else:
    print('两个数据源价格一致 ✓')
