import nbformat, json, os

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# 找到 cell-10 和 cell-11
for i, cell in enumerate(nb.cells):
    cid = cell.get('id', str(i))
    if cid == 'cell-10':
        print('=== cell-10 源码 ===')
        print(cell['source'][:500])
        print('...')
    if cid == 'cell-11':
        print('\n=== cell-11 源码 ===')
        print(cell['source'][:300])
