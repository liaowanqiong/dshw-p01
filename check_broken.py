import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 先恢复notebook（从上次运行前的备份）
# 由于当前notebook已经被破坏，我们需要从git或重新下载
# 这里直接用原notebook的方式修复

# 检查所有被修改的cell
for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid in ('c1', 'c2', 'c6', 'c7', 'c8', 'c9', 'c10', 'c12', 'c13', 'c16'):
        src = cell['source']
        if isinstance(src, list):
            joined = ''.join(src)
            # 检查是否粘连了（import pandas as pdimport numpy...）
            if 'import pandas as pdimport' in joined or 'print(' in joined[:50]:
                print(cid + ': BROKEN (lines glued)')
            else:
                print(cid + ': OK (first 60: ' + joined[:60] + ')')
        else:
            print(cid + ': str type, first 60: ' + str(src)[:60])
