import os, sqlite3

print('='*60)
print('作业验收清单')
print('='*60)

# 1
print('\n1. 项目结构')
root_files = [f for f in os.listdir('.') if not f.startswith('.')]
print(f'   根目录文件数: {len(root_files)}')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f'   子目录: {dirs}')

# 2
print('\n2. 数据下载 (data/)')
stock_dir = 'data/stock'
stock_files = sorted([f for f in os.listdir(stock_dir) if f.endswith('.csv')])
print(f'   股票数据: {len(stock_files)} 个文件')
for f in stock_files:
    size = os.path.getsize(os.path.join(stock_dir, f))
    print(f'     {f} ({size//1024} KB)')

index_dir = 'data/index'
index_files = sorted(os.listdir(index_dir))
print(f'   指数数据: {len(index_files)} 个')

macro_dir = 'data/macro'
macro_files = sorted(os.listdir(macro_dir))
print(f'   宏观数据: {len(macro_files)} 个')

# 3
print('\n3. 数据清洗 (data/clean/)')
clean_dir = 'data/clean'
clean_files = sorted(os.listdir(clean_dir))
for f in clean_files:
    fpath = os.path.join(clean_dir, f)
    size = os.path.getsize(fpath)
    print(f'   {f} ({size//1024} KB)')

conn = sqlite3.connect(os.path.join(clean_dir, 'finance.db'))
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f'   SQLite 表数: {len(tables)}')
for t in ['stock_2594', 'stock_600519', 'index_300']:
    cursor.execute(f'SELECT COUNT(*) FROM {t}')
    count = cursor.fetchone()[0]
    print(f'     {t}: {count} 行')
conn.close()

# 4
print('\n4. 合并数据 (data/combined/)')
for f in sorted(os.listdir('data/combined')):
    fpath = os.path.join('data/combined', f)
    print(f'   {f} ({os.path.getsize(fpath)//1024} KB)')

# 5
print('\n5. 输出文件 (output/)')
for f in sorted(os.listdir('output')):
    fpath = os.path.join('output', f)
    print(f'   {f} ({os.path.getsize(fpath)/1024:.1f} KB)')

# 6
print('\n6. Notebook 文件')
for nb in ['01_download.ipynb', '02_clean.ipynb', '03_analysis.ipynb']:
    if os.path.exists(nb):
        size = os.path.getsize(nb)
        print(f'   {nb} ({size//1024} KB)')
    else:
        print(f'   {nb} - MISSING!')

print('\n' + '='*60)
print('验收完成')
print('='*60)
