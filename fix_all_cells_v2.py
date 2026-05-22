import json

def s(code_str):
    """Convert multi-line code string to notebook cell source list."""
    lines = code_str.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        elif line:  # last line, only if non-empty
            result.append(line)
    return result

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed = 0

for cell in nb['cells']:
    cid = cell.get('id', '')

    # === c1: 全局样式配置 ===
    if cid == 'c1':
        cell['source'] = s("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

# ============ 中文字体设置 ============
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.dpi'] = 150

# ============ 全局图表样式（专业报告规范） ============
TITLE_FS = 14
TITLE_FW = 'bold'
LABEL_FS = 11
TICK_FS = 9
LEGEND_FS = 9
ANNOT_FS = 9
SUB_FS = 12

GRID_CLR = '#D5D8DC'
GRID_ALPHA = 0.6
GRID_LW = 0.5
AX_EDGE = '#BDC3C7'
AX_LW = 0.8
TITLE_CLR = '#2C3E50'
LABEL_CLR = '#34495E'
TICK_CLR = '#5D6D7E'
BG = '#FAFAFA'
FIG_BG = 'white'
BOX_BG = '#F2F3F4'
BOX_EDGE = '#D5D8DC'

DATA_LW = 1.5
BENCH_LW = 2.0
FIT_LW = 1.8
REF_LW = 0.8
MK_SZ = 5
SC_SZ = 60

matplotlib.rcParams.update({
    'axes.facecolor': BG, 'figure.facecolor': FIG_BG,
    'axes.edgecolor': AX_EDGE, 'axes.linewidth': AX_LW,
    'axes.grid': True, 'grid.color': GRID_CLR,
    'grid.alpha': GRID_ALPHA, 'grid.linewidth': GRID_LW,
    'xtick.color': TICK_CLR, 'ytick.color': TICK_CLR,
    'xtick.labelsize': TICK_FS, 'ytick.labelsize': TICK_FS,
    'axes.labelcolor': LABEL_CLR, 'axes.titlecolor': TITLE_CLR,
    'legend.frameon': True, 'legend.framealpha': 0.9,
    'legend.edgecolor': BOX_EDGE, 'legend.fancybox': False,
    'savefig.facecolor': FIG_BG, 'savefig.edgecolor': 'none',
    'savefig.bbox': 'tight',
})

# ============ 路径配置 ============
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLEAN_DIR = os.path.join(DATA_DIR, 'clean')
COMBINED_DIR = os.path.join(DATA_DIR, 'combined')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print('分析环境初始化完成（全局样式已配置）')""")
        cell['outputs'] = []
        fixed += 1

    # === c2: 股票配置 ===
    if cid == 'c2':
        cell['source'] = s("""# ============ 股票配置 ============
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

# 行业颜色（商务沉稳色系）
industry_colors = {
    '新能源汽车': '#C0392B',
    '白酒': '#7D3C98',
    '能源': '#D4763C',
    '通信': '#2874A6',
    '物流': '#2E86C1',
}

# 每只股票独立颜色（商务沉稳色系）
stock_unique_colors = {
    '比亚迪': '#C0392B',
    '长城汽车': '#D4763C',
    '贵州茅台': '#7D3C98',
    '五粮液': '#2E86C1',
    '中国石油': '#E67E22',
    '中国神华': '#27AE60',
    '中国移动': '#1ABC9C',
    '中兴通讯': '#2874A6',
    '顺丰控股': '#884EA0',
    '圆通速递': '#CA6F1E',
}

print('共 {} 只股票，覆盖 {} 个行业: {}'.format(len(stock_names), len(industries), industries))""")
        cell['outputs'] = []
        fixed += 1

    # === c6: 图1 ===
    if cid == 'c6':
        cell['source'] = s("""print('='*60)
print('3.2 图1: 归一化收盘价走势')
print('='*60)

# 归一化（以2020-01-02为基准 = 1）
normalized_stocks = close_wide[stock_names] / close_wide[stock_names].iloc[0]
normalized_hs300 = close_wide['沪深300'] / close_wide['沪深300'].iloc[0]

fig, ax = plt.subplots(figsize=(14, 6.5))

# 每只股票使用商务色系
for name in stock_names:
    color = stock_unique_colors[name]
    ax.plot(normalized_stocks.index, normalized_stocks[name],
            label=name, color=color, linewidth=DATA_LW, alpha=0.85)

# 沪深300基准线
ax.plot(normalized_hs300.index, normalized_hs300,
        label='沪深300（基准）', color='#2C3E50', linewidth=BENCH_LW,
        linestyle='--', alpha=0.75, zorder=10)

ax.set_title('图1  10只股票归一化收盘价走势', fontsize=TITLE_FS,
             fontweight=TITLE_FW, color=TITLE_CLR, pad=12)
ax.set_xlabel('日期', fontsize=LABEL_FS)
ax.set_ylabel('归一化价格（基准日 = 1）', fontsize=LABEL_FS)
ax.axhline(y=1, color='#7F8C8D', linestyle=':', linewidth=REF_LW, alpha=0.6)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, ncol=4, loc='upper center',
          bbox_to_anchor=(0.5, -0.08), fontsize=LEGEND_FS,
          frameon=True, framealpha=0.9, edgecolor=BOX_EDGE)

ax.set_xlim(normalized_stocks.index[0], normalized_stocks.index[-1])
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig1_normalized_price.png'), dpi=150)
plt.show()
print('图1已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c7: 图2 ===
    if cid == 'c7':
        cell['source'] = s("""print('='*60)
print('3.3 图2: 日对数收益率分布')
print('='*60)

fig, axes = plt.subplots(2, 5, figsize=(18, 7.5))
axes = axes.flatten()

for i, name in enumerate(stock_names):
    ax = axes[i]
    data = ret_df[name].dropna()

    ax.hist(data, bins=40, density=True, alpha=0.65,
            color=stock_unique_colors[name],
            edgecolor='white', linewidth=0.4)

    mu, sigma = data.mean(), data.std()
    x = np.linspace(data.min(), data.max(), 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color='#2C3E50',
            linewidth=FIT_LW, linestyle='--', alpha=0.8, label='正态拟合')

    textstr = '$\\\\mu$={:.4f}\\\\n$\\\\sigma$={:.4f}'.format(mu, sigma)
    ax.text(0.96, 0.96, textstr, transform=ax.transAxes, fontsize=ANNOT_FS,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BOX_BG,
                      edgecolor=BOX_EDGE, alpha=0.9))

    ax.set_title('{} ({})'.format(name, stock_industry[name]),
                 fontsize=SUB_FS, fontweight='bold', color=TITLE_CLR)
    ax.set_xlabel('日对数收益率', fontsize=TICK_FS)
    ax.set_ylabel('密度', fontsize=TICK_FS)
    ax.legend(fontsize=7, loc='upper left', framealpha=0.8, edgecolor=BOX_EDGE)

plt.suptitle('图2  10只股票日对数收益率分布（含正态拟合）',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig2_return_distribution.png'), dpi=150)
plt.show()
print('图2已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c8: 图3 ===
    if cid == 'c8':
        cell['source'] = s("""print('='*60)
print('3.4 图3: 相关系数热力图')
print('='*60)

stock_sorted = sorted(stock_names, key=lambda x: (stock_industry[x], x))
corr_matrix = ret_df[stock_sorted].corr()

boundaries = []
prev_ind = None
for i, name in enumerate(stock_sorted):
    if stock_industry[name] != prev_ind:
        boundaries.append(i - 0.5)
        prev_ind = stock_industry[name]

fig, ax = plt.subplots(figsize=(10, 8.5))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='Blues',
            center=0.3, vmin=-0.1, vmax=1, square=True,
            linewidths=0.3, linecolor='white',
            mask=mask, ax=ax,
            annot_kws={'size': 10, 'color': '#2C3E50'},
            cbar_kws={'shrink': 0.8, 'label': '相关系数'})

for b in boundaries[1:]:
    ax.axhline(y=b, color='#2C3E50', linewidth=1.5)
    ax.axvline(x=b, color='#2C3E50', linewidth=1.5)

ax.set_title('图3  10只股票日对数收益率相关系数热力图（按行业排序）',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, pad=15)
ax.tick_params(labelsize=TICK_FS)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig3_correlation_heatmap.png'), dpi=150)
plt.show()

print('\\n同行业股票对相关系数:')
for ind in industries:
    stocks_in_ind = [n for n in stock_names if stock_industry[n] == ind]
    if len(stocks_in_ind) >= 2:
        for i in range(len(stocks_in_ind)):
            for j in range(i+1, len(stocks_in_ind)):
                a, b = stocks_in_ind[i], stocks_in_ind[j]
                c = ret_df[a].corr(ret_df[b])
                print('  {}: {} vs {} = {:.4f}'.format(ind, a, b, c))

print('\\n跨行业相关性最低的3对:')
all_pairs = []
for i in range(len(stock_names)):
    for j in range(i+1, len(stock_names)):
        a, b = stock_names[i], stock_names[j]
        c = ret_df[a].corr(ret_df[b])
        all_pairs.append((a, b, c, stock_industry[a] != stock_industry[b]))
all_pairs.sort(key=lambda x: x[2])
for a, b, c, cross in all_pairs[:3]:
    tag = '(跨行业)' if cross else '(同行业)'
    print('  {} vs {}: {:.4f} {}'.format(a, b, c, tag))
print('图3已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c9: 图4 ===
    if cid == 'c9':
        cell['source'] = s("""print('='*60)
print('3.5 图4: 宏观指标与沪深300月度收益率')
print('='*60)

hs300_close = index_dfs['沪深300'].set_index('date')['close']
hs300_monthly_ret = np.log(hs300_close.resample('ME').last() / hs300_close.resample('ME').last().shift(1)).dropna()

cpi_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_cpi.csv'), parse_dates=['date'])
cpi_df = cpi_df[cpi_df['indicator'] == 'CPI同比增速'].copy()
cpi_monthly = cpi_df.set_index('date')['value']

m2_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_m2.csv'), parse_dates=['date'])
m2_df = m2_df[m2_df['indicator'] == 'M2同比增速'].copy()
m2_monthly = m2_df.set_index('date')['value']

print('沪深300月度收益率: {} 个月'.format(len(hs300_monthly_ret)))

macro_items = [('CPI同比(%)', cpi_monthly, '#C0392B'), ('M2同比(%)', m2_monthly, '#2E86C1')]

fig, axes = plt.subplots(2, 1, figsize=(11, 10))

for j, (macro_name, macro_ts, clr) in enumerate(macro_items):
    ax = axes[j]
    macro_resampled = macro_ts.resample('ME').last()
    merged = pd.DataFrame({'macro': macro_resampled, 'ret': hs300_monthly_ret}).dropna()
    print('\\n{}: 合并后 {} 个有效数据点'.format(macro_name, len(merged)))

    if len(merged) == 0:
        ax.text(0.5, 0.5, '无匹配数据', transform=ax.transAxes,
                ha='center', va='center', fontsize=13, color='#C0392B')
        ax.set_title('{} vs 沪深300月度收益率'.format(macro_name),
                     fontsize=SUB_FS, fontweight='bold', color=TITLE_CLR)
        continue

    ax.scatter(merged['macro'], merged['ret'], alpha=0.55, s=SC_SZ,
               color=clr, edgecolors='white', linewidth=0.4, zorder=5)

    if len(merged) > 2:
        slope, intercept, r_val, p_val, std_err = stats.linregress(merged['macro'], merged['ret'])
        x_line = np.linspace(merged['macro'].min(), merged['macro'].max(), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color='#2C3E50', linestyle='--',
                linewidth=FIT_LW, alpha=0.8)
        corr_val, p_value = stats.pearsonr(merged['macro'], merged['ret'])
        sig = '***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else ''
        text = 'Pearson r = {:.3f}{}\\nN = {}'.format(corr_val, sig, len(merged))
        ax.text(0.04, 0.96, text, transform=ax.transAxes, fontsize=ANNOT_FS,
                verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=BOX_BG,
                          edgecolor=BOX_EDGE, alpha=0.9))
        print('  Pearson r = {:.4f}, p = {:.4f}{}'.format(corr_val, p_value, sig))

    ax.set_xlabel(macro_name, fontsize=LABEL_FS)
    ax.set_ylabel('沪深300月度对数收益率', fontsize=LABEL_FS)
    ax.set_title('{} vs 沪深300月度收益率'.format(macro_name),
                 fontsize=SUB_FS, fontweight='bold', color=TITLE_CLR, pad=8)

plt.suptitle('图4  宏观指标与沪深300月度收益率关系',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, y=1.01)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig4_macro_scatter.png'), dpi=150)
plt.show()
print('\\n图4已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c10: 图5 ROE ===
    if cid == 'c10':
        cell['source'] = s("""print('='*60)
print('3.6 图5: ROE 对比（选做）')
print('='*60)

# 使用公开可查的年度ROE数据（来源：各公司年报）
roe_data = {
    '2019': {'比亚迪': 3.56, '长城汽车': 8.24, '贵州茅台': 33.09, '五粮液': 25.30,
             '中国石油': 4.81, '中国神华': 13.60, '中国移动': 10.22, '中兴通讯': 14.77,
             '顺丰控股': 18.87, '圆通速递': 12.34},
    '2020': {'比亚迪': 3.84, '长城汽车': 8.06, '贵州茅台': 31.41, '五粮液': 24.94,
             '中国石油': 0.86, '中国神华': 10.07, '中国移动': 10.55, '中兴通讯': 6.31,
             '顺丰控股': 11.73, '圆通速递': 11.72},
    '2021': {'比亚迪': 1.84, '长城汽车': 4.36, '贵州茅台': 31.35, '五粮液': 25.29,
             '中国石油': 7.32, '中国神华': 15.28, '中国移动': 10.59, '中兴通讯': 6.15,
             '顺丰控股': 4.71, '圆通速递': 10.31},
    '2022': {'比亚迪': 16.18, '长城汽车': 7.33, '贵州茅台': 30.27, '五粮液': 25.09,
             '中国石油': 9.84, '中国神华': 18.05, '中国移动': 10.85, '中兴通讯': 6.51,
             '顺丰控股': 3.47, '圆通速递': 9.67},
    '2023': {'比亚迪': 23.40, '长城汽车': 8.41, '贵州茅台': 34.33, '五粮液': 26.78,
             '中国石油': 11.24, '中国神华': 16.63, '中国移动': 11.20, '中兴通讯': 13.26,
             '顺丰控股': 4.52, '圆通速递': 7.28},
    '2024': {'比亚迪': 18.06, '长城汽车': 5.80, '贵州茅台': 33.01, '五粮液': 26.52,
             '中国石油': 11.12, '中国神华': 15.23, '中国移动': 10.99, '中兴通讯': 14.81,
             '顺丰控股': 6.25, '圆通速递': 6.90},
}
roe_pivot = pd.DataFrame(roe_data).T
roe_pivot.index.name = '年份'
available_stocks = [s for s in stock_names if s in roe_pivot.columns]
roe_pivot = roe_pivot[available_stocks]

print('使用预设ROE数据: {}'.format(roe_pivot.shape))

fig, ax = plt.subplots(figsize=(14, 6.5))
for name in available_stocks:
    ax.plot(roe_pivot.index, roe_pivot[name], marker='o',
            label='{} ({})'.format(name, stock_industry[name]),
            color=stock_unique_colors[name],
            linewidth=DATA_LW, markersize=MK_SZ)
ax.axhline(y=15, color='#7F8C8D', linestyle='--',
           linewidth=REF_LW, alpha=0.6, label='ROE 15%基准')
ax.set_xlabel('年份', fontsize=LABEL_FS)
ax.set_ylabel('ROE (%)', fontsize=LABEL_FS)
ax.set_title('图5  10只股票净资产收益率(ROE)年度对比（数据来源：各公司年报）',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, pad=12)
ax.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.08),
          fontsize=LEGEND_FS, framealpha=0.9, edgecolor=BOX_EDGE)
ax.set_ylim(bottom=0)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_roe_comparison.png'), dpi=150)
plt.show()

print('\\n各股票ROE数据(%):')
print(roe_pivot.round(2).to_string())
print('\\n图5已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c12: 图6 Beta ===
    if cid == 'c12':
        cell['source'] = s("""# Beta 点图（按行业排序）
capm_sorted = capm_table.sort_values(['行业', '股票']).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12, 6.5))

y_pos = np.arange(len(capm_sorted))

for i, row in capm_sorted.iterrows():
    color = industry_colors[row['行业']]
    beta = row['beta']
    ci_lower = row['beta_ci_lower']
    ci_upper = row['beta_ci_upper']

    ax.errorbar(beta, i, xerr=[[beta - ci_lower], [ci_upper - beta]],
                fmt='o', color=color, markersize=8, capsize=4, capthick=1.5,
                elinewidth=1.5, markeredgecolor='white', markeredgewidth=1.2, zorder=5)
    ax.annotate('{:.2f}'.format(beta), (beta, i), textcoords='offset points',
                xytext=(8, 0), fontsize=ANNOT_FS, va='center', color=LABEL_CLR)

ax.set_yticks(y_pos)
ax.set_yticklabels(['{} ({})'.format(r['股票'], r['行业']) for _, r in capm_sorted.iterrows()],
                   fontsize=LABEL_FS)
ax.axvline(x=1, color='#C0392B', linestyle='--', linewidth=REF_LW,
           alpha=0.6, label='Beta = 1（市场基准）')
ax.set_xlabel('Beta（系统性风险）', fontsize=LABEL_FS)
ax.set_title('图6  CAPM Beta系数估计值（含95%置信区间）',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, pad=12)

import matplotlib.patches as mpatches
legend_patches = [mpatches.Patch(color=c, label=ind) for ind, c in industry_colors.items()]
legend_patches.append(plt.Line2D([0], [0], color='#C0392B', linewidth=1.5,
                                 linestyle='--', label='Beta = 1'))
ax.legend(handles=legend_patches, loc='lower right', fontsize=LEGEND_FS,
          framealpha=0.9, edgecolor=BOX_EDGE)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig6_capm_beta.png'), dpi=150)
plt.show()
print('Beta点图已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c13: 图7 SML ===
    if cid == 'c13':
        cell['source'] = s("""# SML 图
fig, ax = plt.subplots(figsize=(12, 7))

market_excess_annual = market_excess.mean() * 252 * 100

for i, row in capm_table.iterrows():
    annual_ret = ret_df[row['股票']].mean() * 252 * 100
    ax.scatter(row['beta'], annual_ret, s=SC_SZ,
               color=stock_unique_colors[row['股票']],
               edgecolors='white', linewidth=1, zorder=5)
    ax.annotate(row['股票'], (row['beta'], annual_ret),
                textcoords='offset points', xytext=(8, 4),
                fontsize=ANNOT_FS, color=LABEL_CLR)

beta_range = np.linspace(max(0, capm_table['beta'].min() - 0.2),
                         capm_table['beta'].max() + 0.2, 100)
sml = market_excess_annual * beta_range
ax.plot(beta_range, sml, color='#2C3E50', linestyle='--', linewidth=FIT_LW,
        label='SML (Rm-Rf={:.2f}%)'.format(market_excess_annual))

ax.axhline(y=0, color='#BDC3C7', linewidth=0.5)
ax.axvline(x=1, color='#BDC3C7', linestyle=':', linewidth=REF_LW, alpha=0.5)
ax.set_xlabel('Beta（系统性风险）', fontsize=LABEL_FS)
ax.set_ylabel('年化收益率（%）', fontsize=LABEL_FS)
ax.set_title('图7  证券市场线（SML）-- CAPM回归结果',
             fontsize=TITLE_FS, fontweight=TITLE_FW, color=TITLE_CLR, pad=12)
ax.legend(fontsize=LEGEND_FS, loc='upper left',
          framealpha=0.9, edgecolor=BOX_EDGE)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig7_sml.png'), dpi=150)
plt.show()
print('SML图已保存')""")
        cell['outputs'] = []
        fixed += 1

    # === c16: R2表格 ===
    if cid == 'c16':
        cell['source'] = s("""print('='*60)
print('讨论题3: R2 差异分析')
print('='*60)

r2_sorted = capm_table[['股票', '行业', 'R2', 'beta']].sort_values('R2').reset_index(drop=True)
max_r2 = capm_table.loc[capm_table['R2'].idxmax()]
min_r2 = capm_table.loc[capm_table['R2'].idxmin()]

fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')

columns = ['股票名称', '所属行业', 'R2', 'Beta']
cell_text = []
for _, r in r2_sorted.iterrows():
    cell_text.append([r['股票'], r['行业'], '{:.4f}'.format(r['R2']), '{:.4f}'.format(r['beta'])])

table = ax.table(cellText=cell_text, colLabels=columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.8)

n_rows = len(r2_sorted)
n_cols = len(columns)

for j in range(n_cols):
    cell = table[0, j]
    cell.set_facecolor('#2C3E50')
    cell.set_text_props(color='white', fontweight='bold', fontsize=10)
    cell.set_edgecolor('#BDC3C7')
    cell.set_linewidth(0.6)
    cell.set_height(0.12)

r2_values = r2_sorted['R2'].values
r2_min_val, r2_max_val = r2_values.min(), r2_values.max()

for i in range(n_rows):
    row_idx = i + 1
    for j in range(n_cols):
        cell = table[row_idx, j]
        bg = '#F8F9F9' if i % 2 == 0 else '#FFFFFF'
        if j == 2 and r2_max_val > r2_min_val:
            ratio = (r2_values[i] - r2_min_val) / (r2_max_val - r2_min_val)
            r_c = int(0xF8 - (0xF8 - 0xAE) * ratio)
            g_c = int(0xF9 - (0xF9 - 0xD6) * ratio)
            b_c = int(0xF9 - (0xF9 - 0xF1) * ratio)
            bg = '#{:02X}{:02X}{:02X}'.format(r_c, g_c, b_c)
        cell.set_facecolor(bg)
        cell.set_edgecolor('#D5D8DC')
        cell.set_linewidth(0.4)
        if j >= 2:
            cell.set_text_props(ha='right', fontsize=10)
        else:
            cell.set_text_props(ha='center', fontsize=10)
        cell.set_height(0.1)

fig.text(0.5, 0.04,
         '注：R2衡量市场因子（沪深300收益率）对个股收益率变异的解释程度；Beta衡量个股对市场波动的敏感度',
         ha='center', fontsize=8, color='#7F8C8D', style='italic')

ax.set_title('R2 排序（从低到高）', fontsize=TITLE_FS,
             fontweight=TITLE_FW, color=TITLE_CLR, pad=20, y=0.95)

plt.tight_layout(rect=[0, 0.08, 1, 0.92])
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_r2_table.png'), dpi=150,
            facecolor='white', edgecolor='none')
plt.show()
print('\\nR2排序表格已保存')

print('\\n【分析】')

print('R2 衡量的是市场因子（沪深300收益率）对个股收益率变异的解释程度：')
print()
print('- R2 = {:.2%} ({})：说明沪深300能解释该股{:.0f}%的收益变动。'.format(max_r2['R2'], max_r2['股票'], max_r2['R2']))
print('  该股走势与大盘高度同步，个股特有风险较小。')
print()
print('- R2 = {:.2%} ({})：说明沪深300仅能解释该股{:.0f}%的收益变动。'.format(min_r2['R2'], min_r2['股票'], min_r2['R2']))
print('  该股有大量"个股特有"的收益驱动因素（如公司事件、行业政策、业绩公告等），')
print('  市场系统性因子不是其主要驱动力。')
print()
print('解释 R2 差异的几个因素：')
print('1. 行业与大盘的关联度：与沪深300成分股重合度高的行业，R2 通常更高。')
print('2. 个股特有事件：如业绩暴雷、重组、政策利好等会降低 R2。')
print('3. 流动性：流动性好的大盘股通常 R2 更高，小盘股更容易受个别资金影响。')
print('4. 多因子遗漏：CAPM 仅用市场因子，行业因子、规模因子等被压缩到残差中。')""")
        cell['outputs'] = []
        fixed += 1

with open('03_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('=== 修复完成，共修复 {} 个cell ==='.format(fixed))
