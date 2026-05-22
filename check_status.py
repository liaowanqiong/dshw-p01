import sqlite3, os, pandas as pd

conn = sqlite3.connect('data/clean/finance.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print('DB tables:', tables)

cur.execute('PRAGMA table_info(stock_2594)')
cols = [c[1] for c in cur.fetchall()]
print('stock_2594 cols:', cols)

cur.execute('PRAGMA table_info(index_300)')
cols2 = [c[1] for c in cur.fetchall()]
print('index_300 cols:', cols2)

# Check for is_extreme / outlier / daily_return columns
for t in ['stock_2594', 'stock_600519']:
    cur.execute(f'PRAGMA table_info({t})')
    all_cols = [c[1] for c in cur.fetchall()]
    has_extreme = 'is_extreme' in all_cols or 'outlier' in all_cols
    has_ret = 'daily_return' in all_cols
    print(f'{t}: has_extreme={has_extreme}, has_daily_return={has_ret}, cols={all_cols}')

conn.close()

# Check clean CSV files
for f in sorted(os.listdir('data/clean')):
    if f.endswith('.csv'):
        df = pd.read_csv(f'data/clean/{f}', nrows=1)
        print(f'CSV {f}: {list(df.columns)}')
