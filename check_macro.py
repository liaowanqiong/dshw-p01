"""Check CPI and M2 data in detail - date range, indicators, values."""
import pandas as pd

# CPI
cpi = pd.read_csv('data/macro/macro_cpi.csv')
print("=== CPI ===")
print(f"Total rows: {len(cpi)}")
print(f"Unique indicators: {cpi['indicator'].unique()}")
print(f"Date range: {cpi['date'].min()} ~ {cpi['date'].max()}")
cpi['date'] = pd.to_datetime(cpi['date'])
print(f"Date range (parsed): {cpi['date'].min()} ~ {cpi['date'].max()}")
print(cpi.head(10))
print()

# M2
m2 = pd.read_csv('data/macro/macro_m2.csv')
print("=== M2 ===")
print(f"Total rows: {len(m2)}")
print(f"Unique indicators: {m2['indicator'].unique()}")
print(f"Date range: {m2['date'].min()} ~ {m2['date'].max()}")
m2['date'] = pd.to_datetime(m2['date'])
print(f"Date range (parsed): {m2['date'].min()} ~ {m2['date'].max()}")
print(m2.head(10))
print()

# Check what the notebook code expects
print("=== Notebook expects ===")
print("CPI: indicator == '全国-当月同比'")
print("M2: indicator == '货币和准货币(M2)-同比'")
print()
print(f"CPI has '全国-当月同比': {('全国-当月同比' in cpi['indicator'].values)}")
print(f"M2 has '货币和准货币(M2)-同比': {('货币和准货币(M2)-同比' in m2['indicator'].values)}")
