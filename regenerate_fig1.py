import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

BASE_DIR = os.getcwd()
CLEAN_DIR = os.path.join(BASE_DIR, 'data', 'clean')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.dpi'] = 150

# 股票配置
stock_config = {
    '002594': {'name': '比亚迪'}, '601633': {'name': '长城汽车'},
    '600519': {'name': '贵州茅台'}, '000858': {'name': '五粮液'},
    '601857': {'name': '中国石油'}, '601088': {'name': '中国神华'},
    '600941': {'name': '中国移动'}, '000063': {'name': '中兴通讯'},
    '002352': {'name': '顺丰控股'}, '600233': {'name': '圆通速递'},
}
stock_names = [v['name'] for v in stock_config.values()]

stock_unique_colors = {
    '比亚迪': '#e6194b', '长城汽车': '#f58231', '贵州茅台': '#911eb4',
    '五粮液': '#4363d8', '中国石油': '#f032e6', '中国神华': '#bfef45',
    '中国移动': '#fabed4', '中兴通讯': '#469990', '顺丰控股': '#dcbeff',
    '圆通速递': '#9A6324',
}

# 加载宽表
close_wide = pd.read_csv(os.path.join(CLEAN_DIR, 'stock_close_wide.csv'),
                         parse_dates=['date'], index_col='date')

print('=== 沪深300基准线数据检查 ===')
print('宽表日期范围:', close_wide.index.min().date(), '~', close_wide.index.max().date())
print('基准日(iloc[0]):', close_wide.index[0].date())
print('基准日沪深300收盘价:', close_wide['沪深300'].iloc[0])
print('归一化后基准日值:', round(close_wide['沪深300'].iloc[0] / close_wide['沪深300'].iloc[0], 4))

# 归一化
normalized_stocks = close_wide[stock_names] / close_wide[stock_names].iloc[0]
normalized_hs300 = close_wide['沪深300'] / close_wide['沪深300'].iloc[0]

print('\n沪深300归一化序列统计:')
hs_min_idx = normalized_hs300.idxmin()
hs_max_idx = normalized_hs300.idxmax()
print('  最小值:', round(normalized_hs300.min(), 4), '日期:', hs_min_idx.date())
print('  最大值:', round(normalized_hs300.max(), 4), '日期:', hs_max_idx.date())
print('  末值:', round(normalized_hs300.iloc[-1], 4))

# 画图
fig, ax = plt.subplots(figsize=(14, 7))

for name in stock_names:
    color = stock_unique_colors[name]
    ax.plot(normalized_stocks.index, normalized_stocks[name],
            label=name, color=color, linewidth=1.8, alpha=0.9)

ax.plot(normalized_hs300.index, normalized_hs300,
        label='沪深300(基准)', color='black', linewidth=2.5, linestyle='--', alpha=0.7)

ax.set_title('10只股票归一化收盘价走势（基准=1，叠加沪深300）', fontsize=16, fontweight='bold')
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('归一化价格', fontsize=12)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.axhline(y=1, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
plt.tight_layout()

fp = os.path.join(OUTPUT_DIR, 'fig1_normalized_price.png')
fig.savefig(fp, dpi=150, bbox_inches='tight')
plt.close(fig)
print('\n图1已重新保存至:', fp)
print('文件大小:', os.path.getsize(fp), 'bytes')
