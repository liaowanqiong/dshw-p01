import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid in ('cell-10', 'cell-11'):
        print('=== ' + cid + ' ===')
        print(''.join(cell['source']))
        print('\n' + '='*60 + '\n')
