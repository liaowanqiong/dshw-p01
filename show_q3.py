import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    cid = cell.get('id', '')
    src = ''.join(cell.get('source', []))
    if cid == 'c16' and '讨论题3' in src:
        print(src)
