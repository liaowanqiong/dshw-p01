import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Print full source of key cells
targets = {
    'h5': 'fig1 解读',
    'h7': 'fig2 解读',
    'h9': 'fig3 解读',
    'h11': 'fig4 解读',
    'h13': 'fig5 解读',
    'h10': 'fig4 markdown header',
    'c10': 'fig5 ROE code',
    'c9': 'fig4 code',
    'c14': '讨论题1 code',
    'c15': '讨论题2 code',
    'c16': '讨论题3 code',
}

for i, cell in enumerate(nb['cells']):
    cid = cell.get('id', '?')
    if cid in targets:
        src = ''.join(cell.get('source', []))
        print(f"\n{'='*60}")
        print(f"Cell {i} [{cell['cell_type']}] id={cid} -- {targets[cid]}")
        print(f"{'='*60}")
        print(src)
