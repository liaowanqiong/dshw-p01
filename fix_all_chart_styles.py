"""
全局图表样式整改脚本
统一所有图表的配色、字体、布局、装饰，符合专业数据分析报告标准
"""
import json

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# ============================================================
# 全局配色体系：商务沉稳色系
# ============================================================
# 10只股票颜色：低饱和度、区分度高、商务感
NEW_STOCK_COLORS = {
    '比亚迪': '#C0392B',      # 深砖红
    '长城汽车': '#D4763C',    # 赤陶橙
    '贵州茅台': '#7D3C98',    # 深紫
    '五粮液': '#2E86C1',      # 钢蓝
    '中国石油': '#E67E22',    # 深橙
    '中国神华': '#27AE60',    # 翡翠绿
    '中国移动': '#1ABC9C',    # 青色
    '中兴通讯': '#2874A6',    # 藏蓝
    '顺丰控股': '#884EA0',    # 紫藤
    '圆通速递': '#CA6F1E',    # 琥珀
}

# 行业颜色：更沉稳
NEW_INDUSTRY_COLORS = {
    '新能源汽车': '#C0392B',
    '白酒': '#7D3C98',
    '能源': '#D4763C',
    '通信': '#2874A6',
    '物流': '#2E86C1',
}

# ============================================================
# 辅助函数：替换 cell source
# ============================================================
def set_cell_source(nb, cell_id, new_source):
    for cell in nb['cells']:
        cid = cell.get('id', '')
        if cid == cell_id:
            cell['source'] = new_source if isinstance(new_source, str) else new_source
            cell['outputs'] = []  # 清空旧输出
            return True
    return False

# ============================================================
# 1. 修改 cell-1：添加全局样式配置
# ============================================================
OLD_C1 = """import pandas as pd
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

# ============ 路径配置 ============
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLEAN_DIR = os.path.join(DATA_DIR, 'clean')
COMBINED_DIR = os.path.join(DATA_DIR, 'combined')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print('分析环境初始化完成')"""

NEW_C1 = """import pandas as pd
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
# 字体
TITLE_FONTSIZE = 14
TITLE_FONTWEIGHT = 'bold'
LABEL_FONTSIZE = 11
TICK_FONTSIZE = 9
LEGEND_FONTSIZE = 9
ANNOT_FONTSIZE = 9
SUBTITLE_FONTSIZE = 12

# 颜色
GRID_COLOR = '#D5D8DC'
GRID_ALPHA = 0.6
GRID_LINEWIDTH = 0.5
AXES_EDGE_COLOR = '#BDC3C7'
AXES_LINEWIDTH = 0.8
TITLE_COLOR = '#2C3E50'
LABEL_COLOR = '#34495E'
TICK_COLOR = '#5D6D7E'
BG_COLOR = '#FAFAFA'
FIG_FACE_COLOR = 'white'
ANNOT_BOX_COLOR = '#F2F3F4'
ANNOT_EDGE_COLOR = '#D5D8DC'

# 线型
DATA_LINE_WIDTH = 1.5
BENCHMARK_LINE_WIDTH = 2.0
FIT_LINE_WIDTH = 1.8
REFERENCE_LINE_WIDTH = 0.8

# 标记
MARKER_SIZE = 5
SCATTER_SIZE = 60

# 设置全局 rcParams
matplotlib.rcParams.update({
    'axes.facecolor': BG_COLOR,
    'figure.facecolor': FIG_FACE_COLOR,
    'axes.edgecolor': AXES_EDGE_COLOR,
    'axes.linewidth': AXES_LINEWIDTH,
    'axes.grid': True,
    'grid.color': GRID_COLOR,
    'grid.alpha': GRID_ALPHA,
    'grid.linewidth': GRID_LINEWIDTH,
    'xtick.color': TICK_COLOR,
    'ytick.color': TICK_COLOR,
    'xtick.labelsize': TICK_FONTSIZE,
    'ytick.labelsize': TICK_FONTSIZE,
    'axes.labelcolor': LABEL_COLOR,
    'axes.titlecolor': TITLE_COLOR,
    'legend.frameon': True,
    'legend.framealpha': 0.9,
    'legend.edgecolor': ANNOT_EDGE_COLOR,
    'legend.fancybox': False,
    'savefig.facecolor': FIG_FACE_COLOR,
    'savefig.edgecolor': 'none',
    'savefig.bbox': 'tight',
})

# ============ 路径配置 ============
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLEAN_DIR = os.path.join(DATA_DIR, 'clean')
COMBINED_DIR = os.path.join(DATA_DIR, 'combined')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print('分析环境初始化完成（全局样式已配置）')"""

# ============================================================
# 2. 修改 cell-3：股票颜色配置
# ============================================================
OLD_C3_STOCK = """stock_unique_colors = {
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
}"""

NEW_C3_STOCK = """stock_unique_colors = {
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
}"""

OLD_C3_INDUSTRY = """industry_colors = {
    '新能源汽车': '#e74c3c',
    '白酒': '#9b59b6',
    '能源': '#e67e22',
    '通信': '#2ecc71',
    '物流': '#3498db'
}"""

NEW_C3_INDUSTRY = """industry_colors = {
    '新能源汽车': '#C0392B',
    '白酒': '#7D3C98',
    '能源': '#D4763C',
    '通信': '#2874A6',
    '物流': '#2E86C1',
}"""

# ============================================================
# 3. 修改 cell-10 (图1)：归一化收盘价走势
# ============================================================
NEW_C6 = """print('='*60)
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
            label=name, color=color, linewidth=DATA_LINE_WIDTH, alpha=0.85)

# 沪深300基准线
ax.plot(normalized_hs300.index, normalized_hs300,
        label='沪深300（基准）', color='#2C3E50', linewidth=BENCHMARK_LINE_WIDTH,
        linestyle='--', alpha=0.75, zorder=10)

# 标题与轴标签
ax.set_title('图1  10只股票归一化收盘价走势', fontsize=TITLE_FONTSIZE,
             fontweight=TITLE_FONTWEIGHT, color=TITLE_COLOR, pad=12)
ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE)
ax.set_ylabel('归一化价格（基准日 = 1）', fontsize=LABEL_FONTSIZE)

# 参考线 y=1
ax.axhline(y=1, color='#7F8C8D', linestyle=':', linewidth=REFERENCE_LINE_WIDTH, alpha=0.6)

# 图例：置于底部，水平排列
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, ncol=4, loc='upper center',
          bbox_to_anchor=(0.5, -0.08), fontsize=LEGEND_FONTSIZE,
          frameon=True, framealpha=0.9, edgecolor=ANNOT_EDGE_COLOR)

ax.set_xlim(normalized_stocks.index[0], normalized_stocks.index[-1])
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig1_normalized_price.png'), dpi=150)
plt.show()
print('图1已保存')"""

# ============================================================
# 4. 修改 cell-13 (图2)：日对数收益率分布
# ============================================================
NEW_C7 = """print('='*60)
print('3.3 图2: 日对数收益率分布')
print('='*60)

fig, axes = plt.subplots(2, 5, figsize=(18, 7.5))
axes = axes.flatten()

for i, name in enumerate(stock_names):
    ax = axes[i]
    data = ret_df[name].dropna()

    # 直方图
    ax.hist(data, bins=40, density=True, alpha=0.65,
            color=stock_unique_colors[name],
            edgecolor='white', linewidth=0.4)

    # 正态拟合曲线
    mu, sigma = data.mean(), data.std()
    x = np.linspace(data.min(), data.max(), 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color='#2C3E50',
            linewidth=FIT_LINE_WIDTH, linestyle='--', alpha=0.8, label='正态拟合')

    # 标注均值和标准差
    textstr = '$\\mu$={:.4f}\\n$\\sigma$={:.4f}'.format(mu, sigma)
    ax.text(0.96, 0.96, textstr, transform=ax.transAxes, fontsize=ANNOT_FONTSIZE,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ANNOT_BOX_COLOR,
                      edgecolor=ANNOT_EDGE_COLOR, alpha=0.9))

    ax.set_title('{} ({})'.format(name, stock_industry[name]),
                 fontsize=SUBTITLE_FONTSIZE, fontweight='bold', color=TITLE_COLOR)
    ax.set_xlabel('日对数收益率', fontsize=TICK_FONTSIZE)
    ax.set_ylabel('密度', fontsize=TICK_FONTSIZE)
    ax.legend(fontsize=7, loc='upper left', framealpha=0.8, edgecolor=ANNOT_EDGE_COLOR)

plt.suptitle('图2  10只股票日对数收益率分布（含正态拟合）',
             fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT,
             color=TITLE_COLOR, y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig2_return_distribution.png'), dpi=150)
plt.show()
print('图2已保存')"""

# ============================================================
# 5. 修改 cell-16 (图3)：相关系数热力图
# ============================================================
NEW_C8 = """print('='*60)
print('3.4 图3: 相关系数热力图')
print('='*60)

stock_sorted = sorted(stock_names, key=lambda x: (stock_industry[x], x))
corr_matrix = ret_df[stock_sorted].corr()

# 行业分隔线
boundaries = []
prev_ind = None
for i, name in enumerate(stock_sorted):
    if stock_industry[name] != prev_ind:
        boundaries.append(i - 0.5)
        prev_ind = stock_industry[name]

fig, ax = plt.subplots(figsize=(10, 8.5))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

# 使用商务色系热力图
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='Blues',
            center=0.3, vmin=-0.1, vmax=1, square=True,
            linewidths=0.3, linecolor='white',
            mask=mask, ax=ax,
            annot_kws={'size': 10, 'color': '#2C3E50'},
            cbar_kws={'shrink': 0.8, 'label': '相关系数'})

# 行业分隔线
for b in boundaries[1:]:
    ax.axhline(y=b, color='#2C3E50', linewidth=1.5)
    ax.axvline(x=b, color='#2C3E50', linewidth=1.5)

ax.set_title('图3  10只股票日对数收益率相关系数热力图（按行业排序）',
             fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT,
             color=TITLE_COLOR, pad=15)
ax.tick_params(labelsize=TICK_FONTSIZE)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig3_correlation_heatmap.png'), dpi=150)
plt.show()

# 同行业相关性分析
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
print('图3已保存')"""

# ============================================================
# 6. 修改 cell-19 (图4)：宏观指标散点图
# ============================================================
NEW_C9 = """print('='*60)
print('3.5 图4: 宏观指标与沪深300月度收益率')
print('='*60)

# 沪深300月度对数收益率
hs300_close = index_dfs['沪深300'].set_index('date')['close']
hs300_monthly_ret = np.log(hs300_close.resample('ME').last() / hs300_close.resample('ME').last().shift(1)).dropna()

cpi_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_cpi.csv'), parse_dates=['date'])
cpi_df = cpi_df[cpi_df['indicator'] == 'CPI同比增速'].copy()
cpi_monthly = cpi_df.set_index('date')['value']

m2_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'macro', 'macro_m2.csv'), parse_dates=['date'])
m2_df = m2_df[m2_df['indicator'] == 'M2同比增速'].copy()
m2_monthly = m2_df.set_index('date')['value']

print('沪深300月度收益率: {} 个月, {} ~ {}'.format(
    len(hs300_monthly_ret), hs300_monthly_ret.index.min().date(), hs300_monthly_ret.index.max().date()))

macro_items = [('CPI同比(%)', cpi_monthly, '#C0392B'), ('M2同比(%)', m2_monthly, '#2E86C1')]

fig, axes = plt.subplots(2, 1, figsize=(11, 10))

for j, (macro_name, macro_ts, clr) in enumerate(macro_items):
    ax = axes[j]
    macro_resampled = macro_ts.resample('ME').last()
    merged = pd.DataFrame({'macro': macro_resampled, 'ret': hs300_monthly_ret}).dropna()

    if len(merged) == 0:
        ax.text(0.5, 0.5, '无匹配数据', transform=ax.transAxes,
                ha='center', va='center', fontsize=13, color='#C0392B')
        ax.set_title('{} vs 沪深300月度收益率'.format(macro_name),
                     fontsize=SUBTITLE_FONTSIZE, fontweight='bold', color=TITLE_COLOR)
        continue

    ax.scatter(merged['macro'], merged['ret'], alpha=0.55, s=SCATTER_SIZE,
               color=clr, edgecolors='white', linewidth=0.4, zorder=5)

    if len(merged) > 2:
        slope, intercept, r_val, p_val, std_err = stats.linregress(merged['macro'], merged['ret'])
        x_line = np.linspace(merged['macro'].min(), merged['macro'].max(), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color='#2C3E50', linestyle='--',
                linewidth=FIT_LINE_WIDTH, alpha=0.8)
        corr_val, p_value = stats.pearsonr(merged['macro'], merged['ret'])
        sig = '***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else ''
        text = 'Pearson r = {:.3f}{}\\nN = {}'.format(corr_val, sig, len(merged))
        ax.text(0.04, 0.96, text, transform=ax.transAxes, fontsize=ANNOT_FONTSIZE,
                verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=ANNOT_BOX_COLOR,
                          edgecolor=ANNOT_EDGE_COLOR, alpha=0.9))
        print('  {}: Pearson r = {:.4f}, p = {:.4f}{}'.format(macro_name, corr_val, p_value, sig))

    ax.set_xlabel(macro_name, fontsize=LABEL_FONTSIZE)
    ax.set_ylabel('沪深300月度对数收益率', fontsize=LABEL_FONTSIZE)
    ax.set_title('{} vs 沪深300月度收益率'.format(macro_name),
                 fontsize=SUBTITLE_FONTSIZE, fontweight='bold', color=TITLE_COLOR, pad=8)

plt.suptitle('图4  宏观指标与沪深300月度收益率关系',
             fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT,
             color=TITLE_COLOR, y=1.01)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig4_macro_scatter.png'), dpi=150)
plt.show()
print('\\n图4已保存')"""

# ============================================================
# 7. 修改 cell-22 (图5)：ROE 对比
# ============================================================
# 图5有两段代码（try块和except块），都需要修改
# 这里只写except块的代码（因为akshare通常失败），try块也同步修改

NEW_C10_TRY_ROE_PART = """            fig, ax = plt.subplots(figsize=(14, 6.5))
            for name in available_stocks:
                ax.plot(roe_pivot.index, roe_pivot[name], marker='o',
                        label='{} ({})'.format(name, stock_industry[name]),
                        color=stock_unique_colors[name],
                        linewidth=DATA_LINE_WIDTH, markersize=MARKER_SIZE)
            ax.axhline(y=15, color='#7F8C8D', linestyle='--',
                       linewidth=REFERENCE_LINE_WIDTH, alpha=0.6, label='ROE 15%基准')
            ax.set_xlabel('年份', fontsize=LABEL_FONTSIZE)
            ax.set_ylabel('ROE (%)', fontsize=LABEL_FONTSIZE)
            ax.set_title('图5  10只股票净资产收益率(ROE)年度对比',
                         fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT, color=TITLE_COLOR, pad=12)
            ax.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.08),
                      fontsize=LEGEND_FONTSIZE, framealpha=0.9, edgecolor=ANNOT_EDGE_COLOR)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_roe_comparison.png'), dpi=150)
            plt.show()"""

NEW_C10_EXCEPT_ROE_PART = """    fig, ax = plt.subplots(figsize=(14, 6.5))
    for name in available_stocks:
        ax.plot(roe_pivot.index, roe_pivot[name], marker='o',
                label='{} ({})'.format(name, stock_industry[name]),
                color=stock_unique_colors[name],
                linewidth=DATA_LINE_WIDTH, markersize=MARKER_SIZE)
    ax.axhline(y=15, color='#7F8C8D', linestyle='--',
               linewidth=REFERENCE_LINE_WIDTH, alpha=0.6, label='ROE 15%基准')
    ax.set_xlabel('年份', fontsize=LABEL_FONTSIZE)
    ax.set_ylabel('ROE (%)', fontsize=LABEL_FONTSIZE)
    ax.set_title('图5  10只股票净资产收益率(ROE)年度对比（数据来源：各公司年报）',
                 fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT, color=TITLE_COLOR, pad=12)
    ax.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.08),
              fontsize=LEGEND_FONTSIZE, framealpha=0.9, edgecolor=ANNOT_EDGE_COLOR)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_roe_comparison.png'), dpi=150)
    plt.show()"""

# ============================================================
# 8. 修改 cell-27 (图6)：Beta系数点图
# ============================================================
NEW_C12 = """# Beta 点图（按行业排序）
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
                xytext=(8, 0), fontsize=ANNOT_FONTSIZE, va='center', color=LABEL_COLOR)

ax.set_yticks(y_pos)
ax.set_yticklabels(['{} ({})'.format(r['股票'], r['行业']) for _, r in capm_sorted.iterrows()],
                   fontsize=LABEL_FONTSIZE)
ax.axvline(x=1, color='#C0392B', linestyle='--', linewidth=REFERENCE_LINE_WIDTH,
           alpha=0.6, label='Beta = 1（市场基准）')
ax.set_xlabel('Beta（系统性风险）', fontsize=LABEL_FONTSIZE)
ax.set_title('图6  CAPM Beta系数估计值（含95%置信区间）',
             fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT,
             color=TITLE_COLOR, pad=12)

# 行业图例
import matplotlib.patches as mpatches
legend_patches = [mpatches.Patch(color=c, label=ind) for ind, c in industry_colors.items()]
legend_patches.append(plt.Line2D([0], [0], color='#C0392B', linewidth=1.5,
                                 linestyle='--', label='Beta = 1'))
ax.legend(handles=legend_patches, loc='lower right', fontsize=LEGEND_FONTSIZE,
          framealpha=0.9, edgecolor=ANNOT_EDGE_COLOR)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig6_capm_beta.png'), dpi=150)
plt.show()
print('Beta点图已保存')"""

# ============================================================
# 9. 修改 cell-29 (图7)：SML
# ============================================================
NEW_C13 = """# SML 图
fig, ax = plt.subplots(figsize=(12, 7))

market_excess_annual = market_excess.mean() * 252 * 100

for i, row in capm_table.iterrows():
    annual_ret = ret_df[row['股票']].mean() * 252 * 100
    ax.scatter(row['beta'], annual_ret, s=SCATTER_SIZE,
               color=stock_unique_colors[row['股票']],
               edgecolors='white', linewidth=1, zorder=5)
    ax.annotate(row['股票'], (row['beta'], annual_ret),
                textcoords='offset points', xytext=(8, 4),
                fontsize=ANNOT_FONTSIZE, color=LABEL_COLOR)

beta_range = np.linspace(max(0, capm_table['beta'].min() - 0.2),
                         capm_table['beta'].max() + 0.2, 100)
sml = market_excess_annual * beta_range
ax.plot(beta_range, sml, color='#2C3E50', linestyle='--', linewidth=FIT_LINE_WIDTH,
        label='SML (Rm-Rf={:.2f}%)'.format(market_excess_annual))

ax.axhline(y=0, color='#BDC3C7', linewidth=0.5)
ax.axvline(x=1, color='#BDC3C7', linestyle=':', linewidth=REFERENCE_LINE_WIDTH, alpha=0.5)
ax.set_xlabel('Beta（系统性风险）', fontsize=LABEL_FONTSIZE)
ax.set_ylabel('年化收益率（%）', fontsize=LABEL_FONTSIZE)
ax.set_title('图7  证券市场线（SML）-- CAPM回归结果',
             fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT,
             color=TITLE_COLOR, pad=12)
ax.legend(fontsize=LEGEND_FONTSIZE, loc='upper left',
          framealpha=0.9, edgecolor=ANNOT_EDGE_COLOR)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'fig7_sml.png'), dpi=150)
plt.show()
print('SML图已保存')"""

# ============================================================
# 10. 修改 cell-36 (讨论题3 R2表格)
# ============================================================
NEW_C16 = """print('='*60)
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
    cell_text.append([r['股票'], r['行业'], '{:.4f}'.format(r['R2']), '{:.4f}'.format(r['beta'])])

table = ax.table(cellText=cell_text, colLabels=columns,
                 loc='center', cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.8)

n_rows = len(r2_sorted)
n_cols = len(columns)

# 表头：深灰+白字
for j in range(n_cols):
    cell = table[0, j]
    cell.set_facecolor('#2C3E50')
    cell.set_text_props(color='white', fontweight='bold', fontsize=10)
    cell.set_edgecolor('#BDC3C7')
    cell.set_linewidth(0.6)
    cell.set_height(0.12)

# 内容行
r2_values = r2_sorted['R2'].values
r2_min_val, r2_max_val = r2_values.min(), r2_values.max()

for i in range(n_rows):
    row_idx = i + 1
    for j in range(n_cols):
        cell = table[row_idx, j]
        # 交替行
        bg = '#F8F9F9' if i % 2 == 0 else '#FFFFFF'
        # R²条件格式
        if j == 2 and r2_max_val > r2_min_val:
            ratio = (r2_values[i] - r2_min_val) / (r2_max_val - r2_min_val)
            # 从 #F8F9F9 到 #AED6F1（浅蓝）
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

# 脚注
fig.text(0.5, 0.04,
         '注：R²衡量市场因子（沪深300收益率）对个股收益率变异的解释程度；Beta衡量个股对市场波动的敏感度',
         ha='center', fontsize=8, color='#7F8C8D', style='italic')

ax.set_title('R² 排序（从低到高）', fontsize=TITLE_FONTSIZE,
             fontweight=TITLE_FONTWEIGHT, color=TITLE_COLOR, pad=20, y=0.95)

plt.tight_layout(rect=[0, 0.08, 1, 0.92])
fig.savefig(os.path.join(OUTPUT_DIR, 'fig_r2_table.png'), dpi=150,
            facecolor='white', edgecolor='none')
plt.show()
print('\\nR²排序表格已保存')

print('\\n【分析】')

R² 衡量的是市场因子（沪深300收益率）对个股收益率变异的解释程度：

- R² = {:.2%} ({})：说明沪深300能解释该股{:.0f}%的收益变动。
  该股走势与大盘高度同步，个股特有风险较小。

- R² = {:.2%} ({})：说明沪深300仅能解释该股{:.0f}%的收益变动。
  该股有大量"个股特有"的收益驱动因素（如公司事件、行业政策、
  业绩公告等），市场系统性因子不是其主要驱动力。

解释 R² 差异的几个因素：
1. 行业与大盘的关联度：与沪深300成分股重合度高的行业，R² 通常更高。
2. 个股特有事件：如业绩暴雷、重组、政策利好等会降低 R²。
3. 流动性：流动性好的大盘股通常 R² 更高，小盘股更容易受个别资金影响。
4. 多因子遗漏：CAPM 仅用市场因子，行业因子、规模因子等被压缩到残差中。'.format(
    max_r2['R2'], max_r2['股票'], max_r2['R2'],
    min_r2['R2'], min_r2['股票'], min_r2['R2']
))"""

# ============================================================
# 执行所有替换
# ============================================================
cells_modified = []

# 逐cell查找并替换
for cell in nb['cells']:
    cid = cell.get('id', '')
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

    # c1: 全局样式
    if cid == 'c1' and 'import pandas as pd' in src:
        cell['source'] = NEW_C1.split('\n')
        cells_modified.append('c1 (全局样式)')

    # c2: 股票颜色
    if cid == 'c2':
        modified = False
        new_src = src
        if OLD_C3_STOCK.strip() in new_src:
            new_src = new_src.replace(OLD_C3_STOCK, NEW_C3_STOCK)
            modified = True
        if OLD_C3_INDUSTRY.strip() in new_src:
            new_src = new_src.replace(OLD_C3_INDUSTRY, NEW_C3_INDUSTRY)
            modified = True
        if modified:
            cell['source'] = new_src.split('\n')
            cells_modified.append('c2 (股票颜色)')

    # c6 (图1)
    if cid == 'c6' and '归一化收盘价走势' in src:
        cell['source'] = NEW_C6.split('\n')
        cell['outputs'] = []
        cells_modified.append('c6 (图1)')

    # c7 (图2)
    if cid == 'c7' and '日对数收益率分布' in src:
        cell['source'] = NEW_C7.split('\n')
        cell['outputs'] = []
        cells_modified.append('c7 (图2)')

    # c8 (图3)
    if cid == 'c8' and '相关系数热力图' in src:
        cell['source'] = NEW_C8.split('\n')
        cell['outputs'] = []
        cells_modified.append('c8 (图3)')

    # c9 (图4)
    if cid == 'c9' and '宏观指标与沪深300月度收益率' in src:
        cell['source'] = NEW_C9.split('\n')
        cell['outputs'] = []
        cells_modified.append('c9 (图4)')

    # c10 (图5 ROE)
    if cid == 'c10' and 'ROE' in src:
        # 替换两处绘图代码
        new_src = src
        # 替换try块中的绘图部分
        try_old = """            fig, ax = plt.subplots(figsize=(14, 7))
            for name in available_stocks:
                ax.plot(roe_pivot.index, roe_pivot[name], marker='o',
                        label=f'{name} ({stock_industry[name]})',
                        color=stock_unique_colors[name], linewidth=2, markersize=6)
            ax.axhline(y=15, color='red', linestyle='--', linewidth=1, alpha=0.5, label='ROE 15%基准线')
            ax.set_xlabel('年份', fontsize=12)
            ax.set_ylabel('ROE (%)', fontsize=12)
            ax.set_title('10只股票净资产收益率(ROE)年度对比', fontsize=16, fontweight='bold')
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_roe_comparison.png'), dpi=150, bbox_inches='tight')"""
        if try_old in new_src:
            new_src = new_src.replace(try_old, NEW_C10_TRY_ROE_PART)

        # 替换except块中的绘图部分
        except_old = """    fig, ax = plt.subplots(figsize=(14, 7))
    for name in available_stocks:
        ax.plot(roe_pivot.index, roe_pivot[name], marker='o',
                label=f'{name} ({stock_industry[name]})',
                color=stock_unique_colors[name], linewidth=2, markersize=6)
    ax.axhline(y=15, color='red', linestyle='--', linewidth=1, alpha=0.5, label='ROE 15%基准线')
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('ROE (%)', fontsize=12)
    ax.set_title('10只股票净资产收益率(ROE)年度对比（数据来源：各公司年报）', fontsize=16, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_roe_comparison.png'), dpi=150, bbox_inches='tight')"""
        if except_old in new_src:
            new_src = new_src.replace(except_old, NEW_C10_EXCEPT_ROE_PART)

        cell['source'] = new_src.split('\n')
        cell['outputs'] = []
        cells_modified.append('c10 (图5)')

    # c12 (图6 Beta)
    if cid == 'c12' and 'Beta系数估计值' in src:
        cell['source'] = NEW_C12.split('\n')
        cell['outputs'] = []
        cells_modified.append('c12 (图6)')

    # c13 (图7 SML)
    if cid == 'c13' and '证券市场线' in src:
        cell['source'] = NEW_C13.split('\n')
        cell['outputs'] = []
        cells_modified.append('c13 (图7)')

    # c16 (R2表格)
    if cid == 'c16' and 'R² 差异分析' in src:
        cell['source'] = NEW_C16.split('\n')
        cell['outputs'] = []
        cells_modified.append('c16 (R2表格)')

# 保存
with open('03_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('=== 修改完成 ===')
print('已修改的 cell:', len(cells_modified))
for c in cells_modified:
    print('  ', c)
