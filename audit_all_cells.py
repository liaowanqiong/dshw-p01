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

    # Check if code cell has proper line breaks
    if ctype == 'code':
        if '\n' in joined:
            status = 'OK'
        else:
            status = 'BROKEN (no newlines)'
    else:
        status = 'markdown'

    preview = joined[:50].replace('\n', '|')
    print(cid + ' [' + ctype + '] ' + status + ': ' + preview)
