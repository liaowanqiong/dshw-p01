import json

with open('02_clean.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Fix cell that has pct_chg in SQL query
for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if 'SELECT date, open, high, low, close, volume, pct_chg' in src:
        lines = cell['source']
        new_lines = []
        for line in lines:
            line = line.replace(', pct_chg', '')
            line = line.replace(', pct_chg as', ',')
            line = line.replace('pct_chg as 涨跌幅', 'close as 收盘价')
            new_lines.append(line)
        cell['source'] = new_lines
        print('Fixed SQL cell')

    # Fix outlier detection cell to use close-based returns
    if 'detect_outliers_iqr' in src and 'pct_chg' in src and 'daily_return' not in src:
        lines = cell['source']
        new_lines = []
        for line in lines:
            line = line.replace("'pct_chg'", "'daily_return'")
            line = line.replace("df['pct_chg']", "df['close']")
            line = line.replace("df[\"pct_chg\"]", "df[\"close\"]")
            new_lines.append(line)

        # Add daily_return calculation before the loop
        for i, line in enumerate(new_lines):
            if 'for name, df in stock_dfs.items():' in line and 'outlier' in ''.join(new_lines[i:i+5]):
                indent = len(line) - len(line.lstrip())
                prefix = ' ' * indent
                insert_lines = [
                    prefix + '# 对每只股票计算日收益率\n',
                    prefix + 'for name, df in stock_dfs.items():\n',
                    prefix + '    df["daily_return"] = df["close"].pct_change() * 100\n',
                    '\n'
                ]
                new_lines = new_lines[:i] + insert_lines + ['\n', prefix + '# 使用IQR方法检测离群值\n'] + new_lines[i+5:]
                break

        cell['source'] = new_lines
        print('Fixed outlier cell')

with open('02_clean.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Done')
