import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 检查 cell c1 的 source 格式
for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid == 'c1':
        src = cell['source']
        print('type:', type(src))
        if isinstance(src, list):
            print('list length:', len(src))
            print('first 5 items:')
            for s in src[:5]:
                print('  repr:', repr(s[:60]))
        else:
            print('string, first 200:', src[:200])
        break
