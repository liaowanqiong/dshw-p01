"""Fix the broken cell-3 in 03_analysis.ipynb - proper newlines and preserve stock_names definition."""
import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find cell-3 and fix it
for cell in nb['cells']:
    src = ''.join(cell.get('source', []))

    if 'stock_unique_colors' in src and 'industry_colors' in src:
        # Replace entire cell content
        new_code = """# ============ 股票配置 ============
stock_config = {
    '002594': {'name': '比亚迪', 'industry': '新能源汽车'},
    '601633': {'name': '长城汽车', 'industry': '新能源汽车'},
    '600519': {'name': '贵州茅台', 'industry': '白酒'},
    '000858': {'name': '五粮液', 'industry': '白酒'},
    '601857': {'name': '中国石油', 'industry': '能源'},
    '601088': {'name': '中国神华', 'industry': '能源'},
    '600941': {'name': '中国移动', 'industry': '通信'},
    '000063': {'name': '中兴通讯', 'industry': '通信'},
    '002352': {'name': '顺丰控股', 'industry': '物流'},
    '600233': {'name': '圆通速递', 'industry': '物流'},
}

stock_names = [v['name'] for v in stock_config.values()]
stock_industry = {v['name']: v['industry'] for v in stock_config.values()}
industries = sorted(set(stock_industry.values()))

# 行业颜色映射
industry_colors = {
    '新能源汽车': '#e74c3c',
    '白酒': '#9b59b6',
    '能源': '#e67e22',
    '通信': '#2ecc71',
    '物流': '#3498db'
}

# 每只股票独立颜色（图1需要区分每只股票）
stock_unique_colors = {
    '比亚迪': '#e6194b',
    '长城汽车': '#f58231',
    '贵州茅台': '#911eb4',
    '五粮液': '#4363d8',
    '中国石油': '#f032e6',
    '中国神华': '#bfef45',
    '中国移动': '#fabed4',
    '中兴通讯': '#469990',
    '顺丰控股': '#dcbeff',
    '圆通速递': '#9A6324',
}

print(f'共 {len(stock_names)} 只股票，覆盖 {len(industries)} 个行业: {industries}')
print(f'每只股票独立颜色: {len(stock_unique_colors)} 种')"""

        lines = new_code.split('\n')
        cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]]
        print(f"Fixed cell-3: restored stock_names + stock_unique_colors")

    # Also fix fig1 cell to use stock_unique_colors
    if "stock_unique_colors[name]" in src and "normalized_stocks" in src:
        new_fig_code = """print('='*60)
print('3.2 图1: 归一化收盘价走势')
print('='*60)

# 归一化（以第一天为基准 = 1）
normalized_stocks = close_wide[stock_names] / close_wide[stock_names].iloc[0]

# 沪深300归一化
normalized_hs300 = close_wide['沪深300'] / close_wide['沪深300'].iloc[0]

fig, ax = plt.subplots(figsize=(14, 7))

# 每只股票使用独立颜色
for name in stock_names:
    color = stock_unique_colors[name]
    lw = 1.8
    ax.plot(normalized_stocks.index, normalized_stocks[name],
            label=name, color=color, linewidth=lw, alpha=0.9)

# 叠加沪深300
ax.plot(normalized_hs300.index, normalized_hs300,
        label='沪深300(基准)', color='black', linewidth=2.5, linestyle='--', alpha=0.7)

ax.set_title('10只股票归一化收盘价走势（基准=1，叠加沪深300）', fontsize=16, fontweight='bold')
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('归一化价格', fontsize=12)

# 图例: 每只股票独立显示
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

ax.grid(True, alpha=0.3)
ax.axhline(y=1, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
plt.tight_layout()

fig.savefig(os.path.join(OUTPUT_DIR, 'fig1_normalized_price.png'), dpi=150, bbox_inches='tight')
plt.show()
print('图1已保存')"""

        lines = new_fig_code.split('\n')
        cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]]
        print(f"Fixed fig1 cell")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done!")
