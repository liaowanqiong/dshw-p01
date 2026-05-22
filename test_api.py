import akshare as ak
import pandas as pd

print('1. macro_china_industrial_production_yoy')
try:
    df = ak.macro_china_industrial_production_yoy()
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head(5))
except Exception as e:
    print(f'错误: {e}')

print()
print('2. currency_boc_sina 汇率完整数据')
try:
    df = ak.currency_boc_sina(symbol='美元')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    date_col = '日期'
    print(f'日期范围: {df[date_col].min()} ~ {df[date_col].max()}')
    print(df.head(3))
    print(df.tail(3))
except Exception as e:
    print(f'错误: {e}')

print()
print('3. 财务数据接口测试')
try:
    df = ak.stock_financial_analysis_indicator(symbol='600519')
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head(3))
except Exception as e:
    print(f'错误: {e}')
