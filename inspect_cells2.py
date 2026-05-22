import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid == 'cell-10':
        print('=== cell-10 source ===')
        print(''.join(cell['source']))
        break
    if cid == 'cell-11':
        print('\n=== cell-11 source ===')
        print(''.join(cell['source']))
        break
