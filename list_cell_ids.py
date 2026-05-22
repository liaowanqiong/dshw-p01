import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    cid = cell.get('id', 'NO_ID')
    ctype = cell['cell_type']
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    preview = src[:80].replace('\n', ' | ')
    print('Cell {}: id={}, type={}, src={}'.format(i, cid, ctype, preview[:60]))
