import akshare as ak
import pandas as pd

# 1. 汇率 - 尝试另一个接口
print('1. currency_boc_safe')
try:
    df = ak.currency_boc_safe(symbol='美元')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    date_col = df.columns[0]
    print(f'日期范围: {df[date_col].min()} ~ {df[date_col].max()}')
    print(df.head(3))
except Exception as e:
    print(f'错误: {e}')

# 2. 财务数据 - 尝试其他接口
print()
print('2. stock_financial_abstract_ths')
try:
    df = ak.stock_financial_abstract_ths(symbol='600519', indicator='按报告期')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head(5))
except Exception as e:
    print(f'错误: {e}')

print()
print('3. stock_financial_report_sina')
try:
    df = ak.stock_financial_report_sina(stock='600519', symbol='利润表')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head(3))
except Exception as e:
    print(f'错误: {e}')

print()
print('4. stock_balance_sheet_by_report_em')
try:
    df = ak.stock_balance_sheet_by_report_em(symbol='SH600519')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head(3))
except Exception as e:
    print(f'错误: {e}')
