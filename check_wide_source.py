import pandas as pd
import os

# 检查 stock_close_wide.csv 中沪深300列的来源
fp = 'data/clean/stock_close_wide.csv'
df = pd.read_csv(fp, parse_dates=['date'])
print('列名:', list(df.columns))
print('行数:', len(df))
print('沪深300 非空数:', df['沪深300'].notna().sum())
print('沪深300 首值:', df['沪深300'].dropna().iloc[0])
print('沪深300 末值:', df['沪深300'].dropna().iloc[-1])

# 对比 index_300_clean.csv
df3 = pd.read_csv('data/clean/index_300_clean.csv', parse_dates=['date'])
print('\nindex_300_clean.csv:')
print('行数:', len(df3))
print('close 首值:', df3['close'].iloc[0])
print('close 末值:', df3['close'].iloc[-1])

# 合并对比
merged = pd.merge(df[['date','沪深300']], df3[['date','close']],
                   left_on='date', right_on='date', how='inner')
merged['diff'] = merged['沪深300'] - merged['close']
print('\n合并后行数:', len(merged))
print('差异描述:')
print(merged['diff'].describe())
