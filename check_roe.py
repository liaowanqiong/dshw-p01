import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell.get('source', []))
        if 'fig5' in src.lower() or 'roe' in src.lower():
            has_output = bool(cell.get('outputs', []))
            print(f'Cell {i}: ROE-related, has_output={has_output}')
            if cell.get('outputs'):
                for out in cell['outputs']:
                    if out.get('text'):
                        text = ''.join(out['text'])[:200]
                        print(f'  Output: {text}')
