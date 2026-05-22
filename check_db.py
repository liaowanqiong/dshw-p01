import sqlite3, os

db_path = os.path.join('data', 'clean', 'finance.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check columns of stock_2594 (actual table name)
cursor.execute('PRAGMA table_info(stock_2594)')
cols = cursor.fetchall()
print('Columns of stock_2594:')
for c in cols:
    print(f'  {c[1]} ({c[2]})')

cursor.execute('SELECT * FROM stock_2594 LIMIT 3')
rows = cursor.fetchall()
print('\nSample data from stock_2594:')
for r in rows:
    print(f'  {r}')

# Check index table
cursor.execute('PRAGMA table_info(index_300)')
cols = cursor.fetchall()
print('\nColumns of index_300:')
for c in cols:
    print(f'  {c[1]} ({c[2]})')

cursor.execute('SELECT * FROM index_300 LIMIT 3')
rows = cursor.fetchall()
print('\nSample data from index_300:')
for r in rows:
    print(f'  {r}')

# Also check if there are clean CSV files
clean_dir = os.path.join('data', 'clean')
for f in sorted(os.listdir(clean_dir)):
    if f.endswith('.csv'):
        fpath = os.path.join(clean_dir, f)
        size = os.path.getsize(fpath)
        print(f'\n{f} ({size} bytes):')

conn.close()
