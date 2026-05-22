"""Replace discussion 3 cell with professional styled table using matplotlib."""
import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_code = r"""print('='*60)
print('讨论题3: R² 差异分析')
print('='*60)

r2_sorted = capm_table[['股票', '行业', 'R2', 'beta']].sort_values('R2').reset_index(drop=True)
max_r2 = capm_table.loc[capm_table['R2'].idxmax()]
min_r2 = capm_table.loc[capm_table['R2'].idxmin()]

# ========== 专业报告样式表格 ==========
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')

columns = ['股票名称', '所属行业', 'R²', 'Beta']
cell_text = []
for _, r in r2_sorted.iterrows():
    cell_text.append([r['股票'], r['行业'], f"{r['R2']:.4f}", f"{r['beta']:.4f}"])

table = ax.table(cellText=cell_text, colLabels=columns,
                 loc='center', cellLoc='center')

# 表格尺寸
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.0, 1.8)

n_rows = len(r2_sorted)
n_cols = len(columns)

# 表头样式：深灰背景+白色加粗
for j in range(n_cols):
    cell = table[0, j]
    cell.set_facecolor('#4A4A4A')
    cell.set_text_props(color='white', fontweight='bold', fontsize=11)
    cell.set_edgecolor('#CCCCCC')
    cell.set_linewidth(0.8)

# 内容行样式
r2_values = r2_sorted['R2'].values
r2_min, r2_max = r2_values.min(), r2_values.max()

for i in range(n_rows):
    row_idx = i + 1  # table row index (0 = header)
    for j in range(n_cols):
        cell = table[row_idx, j]
        # 交替行底色
        if i % 2 == 0:
            bg_color = '#F5F5F5'
        else:
            bg_color = '#FFFFFF'

        # R²列（j=2）条件格式：浅灰→低饱和蓝色渐变
        if j == 2 and r2_max > r2_min:
            ratio = (r2_values[i] - r2_min) / (r2_max - r2_min)
            # 从 #F5F5F5 (浅灰) 到 #A8C6E0 (低饱和蓝)
            r_c = int(0xF5 - (0xF5 - 0xA8) * ratio)
            g_c = int(0xF5 - (0xF5 - 0xC6) * ratio)
            b_c = int(0xF5 - (0xF5 - 0xE0) * ratio)
            bg_color = f'#{r_c:02X}{g_c:02X}{b_c:02X}'

        cell.set_facecolor(bg_color)
        cell.set_edgecolor('#CCCCCC')
        cell.set_linewidth(0.5)

        # 数值列右对齐
        if j >= 2:
            cell.set_text_props(ha='right', fontsize=11)
        else:
            cell.set_text_props(ha='center', fontsize=11)

# 脚注
fig.text(0.5, 0.06,
         '注：R²衡量市场因子（沪深300收益率）对个股收益率变异的解释程度；Beta衡量个股对市场波动的敏感度',
         ha='center', fontsize=9, color='#666666', style='italic')

ax.set_title('R² 排序（从低到高）', fontsize=15, fontweight='bold', pad=20, y=0.95)

plt.tight_layout(rect=[0, 0.1, 1, 0.92])
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_r2_table.png'), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()
print('\nR²排序表格已保存')

print(f'''\n【分析】

R² 衡量的是市场因子（沪深300收益率）对个股收益率变异的解释程度：

- R² = {max_r2['R2']:.2%} ({max_r2['股票']})：说明沪深300能解释该股{max_r2['R2']:.0f}%的收益变动。
  该股走势与大盘高度同步，个股特有风险较小。

- R² = {min_r2['R2']:.2%} ({min_r2['股票']})：说明沪深300仅能解释该股{min_r2['R2']:.0f}%的收益变动。
  该股有大量"个股特有"的收益驱动因素（如公司事件、行业政策、
  业绩公告等），市场系统性因子不是其主要驱动力。

解释 R² 差异的几个因素：
1. 行业与大盘的关联度：与沪深300成分股重合度高的行业，R² 通常更高。
2. 个股特有事件：如业绩暴雷、重组、政策利好等会降低 R²。
3. 流动性：流动性好的大盘股通常 R² 更高，小盘股更容易受个别资金影响。
4. 多因子遗漏：CAPM 仅用市场因子，行业因子、规模因子等被压缩到残差中。''')"""

for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid == 'c16' and '讨论题3' in ''.join(cell.get('source', [])):
        lines = new_code.split('\n')
        cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]]
        print("Fixed discussion 3 cell")
        break
else:
    print("ERROR: cell c16 not found!")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done!")
