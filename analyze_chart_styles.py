import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 提取所有 code cell 的 id 和前几行
for i, cell in enumerate(nb['cells']):
    cid = cell.get('id', f'cell-{i}')
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        lines = src.strip().split('\n')
        # 找包含 plt/fig/ax/table/savefig 的 cell
        chart_keywords = ['plt.subplots', 'fig.savefig', 'sns.heatmap', 'ax.table', 'plt.figure']
        has_chart = any(kw in src for kw in chart_keywords)
        if has_chart:
            print(f'\n=== {cid} (code cell) ===')
            print(f'行数: {len(lines)}')
            # 打印包含关键样式设置的行
            for j, line in enumerate(lines):
                stripped = line.strip()
                if any(kw in line for kw in ['figsize', 'fontsize', 'color=', 'linewidth', 'linestyle',
                    'set_title', 'set_xlabel', 'set_ylabel', 'legend', 'grid', 'savefig',
                    'facecolor', 'edgecolor', 'alpha=', 'bbox_to_anchor', 'rcParams',
                    'fontweight', 'ha=', 'va=', 'marker', 'suptitle',
                    'errorbar', 'scatter', 'axhline', 'axvline',
                    ' cmap', 'annot', 'center=', 'vmin', 'vmax']):
                    print(f'  L{j}: {stripped}')
