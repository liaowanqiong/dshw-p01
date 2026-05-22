"""Fix fig4 cell - use correct indicator names and handle date alignment."""
import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_fig4_code = """print('='*60)
print('3.5 图4: 宏观指标与沪深300月度收益率')
print('='*60)

# 沪深300月度对数收益率
hs300_close = index_dfs['沪深300'].set_index('date')['close']
hs300_monthly_ret = np.log(hs300_close.resample('ME').last() / hs300_close.resample('ME').last().shift(1)).dropna()

# 加载CPI数据 - indicator为 'CPI同比增速'，日期为发布日
cpi_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_cpi.csv'), parse_dates=['date'])
cpi_df = cpi_df[cpi_df['indicator'] == 'CPI同比增速'].copy()
cpi_df['month'] = cpi_df['date'].dt.to_period('M')
cpi_monthly = cpi_df.set_index('date')['value']

# 加载M2数据 - indicator为 'M2同比增速'，日期为月份首日
m2_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_m2.csv'), parse_dates=['date'])
m2_df = m2_df[m2_df['indicator'] == 'M2同比增速'].copy()
m2_df['month'] = m2_df['date'].dt.to_period('M')
m2_monthly = m2_df.set_index('date')['value']

print(f'沪深300月度收益率: {len(hs300_monthly_ret)} 个月, {hs300_monthly_ret.index.min().date()} ~ {hs300_monthly_ret.index.max().date()}')
print(f'CPI数据: {len(cpi_monthly)} 条, {cpi_monthly.index.min().date()} ~ {cpi_monthly.index.max().date()}')
print(f'M2数据: {len(m2_monthly)} 条, {m2_monthly.index.min().date()} ~ {m2_monthly.index.max().date()}')

# 合并并绘图
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

macro_items = [('CPI同比(%)', cpi_monthly, '#e74c3c'), ('M2同比(%)', m2_monthly, '#3498db')]

for j, (macro_name, macro_ts, clr) in enumerate(macro_items):
    ax = axes[j]
    
    # 将宏观数据对齐到月末: 按月重采样取最后值
    macro_resampled = macro_ts.resample('ME').last()
    
    # 合并
    merged = pd.DataFrame({
        'macro': macro_resampled,
        'ret': hs300_monthly_ret
    }).dropna()
    
    print(f'\\n{macro_name}: 合并后 {len(merged)} 个有效数据点')
    
    if len(merged) == 0:
        ax.text(0.5, 0.5, '无匹配数据', transform=ax.transAxes,
                ha='center', va='center', fontsize=14, color='red')
        ax.set_title(f'{macro_name} vs 沪深300月度收益率', fontsize=12, fontweight='bold')
        continue
    
    ax.scatter(merged['macro'], merged['ret'], alpha=0.6, s=50,
               color=clr, edgecolors='white', linewidth=0.5)
    
    if len(merged) > 2:
        # 线性拟合
        slope, intercept, r_val, p_val, std_err = stats.linregress(merged['macro'], merged['ret'])
        x_line = np.linspace(merged['macro'].min(), merged['macro'].max(), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'r--', linewidth=2, alpha=0.8)
        
        # Pearson相关系数
        corr_val, p_value = stats.pearsonr(merged['macro'], merged['ret'])
        sig = '***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else ''
        ax.text(0.05, 0.95, f'Pearson r = {corr_val:.3f}{sig}\\nN = {len(merged)}',
                transform=ax.transAxes, fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        print(f'  Pearson r = {corr_val:.4f}, p = {p_value:.4f}{sig}')
    
    ax.set_xlabel(macro_name, fontsize=11)
    ax.set_ylabel('沪深300月度对数收益率', fontsize=11)
    ax.set_title(f'{macro_name} vs 沪深300月度收益率', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.suptitle('宏观指标与沪深300月度收益率关系', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

fig.savefig(os.path.join(OUTPUT_DIR, 'fig4_macro_scatter.png'), dpi=150, bbox_inches='tight')
plt.show()
print('\\n图4已保存')"""

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if '3.5 图4: 宏观指标与沪深300月度收益率' in src and 'macro_items' in src:
        lines = new_fig4_code.split('\n')
        cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]]
        print("Fixed fig4 cell")
        break
else:
    print("ERROR: Could not find fig4 cell!")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done!")
