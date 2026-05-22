import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    cid = cell.get('id', '')
    ctype = cell['cell_type']
    src = cell['source']
    if isinstance(src, list):
        joined = ''.join(src)
    else:
        joined = src

    if ctype == 'code':
        has_newlines = '\n' in joined
        first_line = joined.split('\n')[0][:50]
        status = 'OK' if has_newlines else 'BROKEN'
        print('{} [code] {}: {}'.format(cid, status, first_line))
