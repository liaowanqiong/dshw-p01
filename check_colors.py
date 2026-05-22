import json
with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'stock_colors' in src:
        has_unique = 'stock_unique_colors' in src
        print(f'Cell {i} ({cell.get("id","?")}): stock_colors={True}, stock_unique_colors={has_unique}')
        print(f'  First 300 chars: {repr(src[:300])}')
        print()
