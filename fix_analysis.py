import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    # Fix cell-6: descriptive stats - use daily_return
    if 'pct_chg' in src and 'ret_data[name]' in src:
        new_lines = []
        for line in cell['source']:
            line = line.replace("'pct_chg'", "'daily_return'")
            line = line.replace("df['pct_chg']", "df['daily_return']")
            line = line.replace('df[\"pct_chg\"]', 'df[\"daily_return\"]')
            line = line.replace('# pct_chg 是百分比，转为小数', '# daily_return 已是百分比，转为小数')
            new_lines.append(line)
        cell['source'] = new_lines
        print('Fixed descriptive stats cell')
    
    # Fix cell-18: CAPM - use daily_return for both stock and market
    if 'market_ret = market_df.set_index' in src and 'pct_chg' in src:
        new_lines = []
        for line in cell['source']:
            line = line.replace("['pct_chg']", "['daily_return']")
            line = line.replace('["pct_chg"]', '["daily_return"]')
            line = line.replace('转为小数', '转为小数（daily_return已是百分比）')
            new_lines.append(line)
        cell['source'] = new_lines
        print('Fixed CAPM cell')

with open('03_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('03_analysis.ipynb fixed and saved')
