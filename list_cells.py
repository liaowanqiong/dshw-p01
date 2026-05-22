import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Print all cell IDs and first line of source
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    ctype = cell.get('cell_type', '?')
    cid = cell.get('id', '?')
    first_line = src.split('\n')[0][:80] if src else '(empty)'
    print(f"Cell {i:2d} [{ctype:8s}] id={cid:8s} | {first_line}")
