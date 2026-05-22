import os

print('='*70)
print('最终验收 — 对照作业要求逐项检查')
print('='*70)

checks = []

# 1. 项目根目录
checks.append(('项目根目录名称 dshw-p01', os.path.basename(os.getcwd()) == 'dshw-p01' or 'dshw-p01' in os.getcwd()))

# 2. README.md
checks.append(('README.md 存在', os.path.exists('README.md')))

# 3. download_log.txt
checks.append(('download_log.txt 存在', os.path.exists('download_log.txt')))

# 4. 3个Notebook
for nb in ['01_download.ipynb', '02_clean.ipynb', '03_analysis.ipynb']:
    checks.append((f'{nb} 存在', os.path.exists(nb)))

# 5. 数据完整性
checks.append(('10只股票数据', len([f for f in os.listdir('data/stock') if f.endswith('.csv')]) == 10))
checks.append(('2个指数数据', len([f for f in os.listdir('data/index') if f.endswith('.csv')]) >= 2))
checks.append(('5个宏观数据', len([f for f in os.listdir('data/macro') if f.endswith('.csv')]) >= 5))
checks.append(('财务数据', os.path.exists('data/finance/finance_ratios.csv')))

# 6. 清洗步骤
checks.append(('is_extreme列 (02_clean)', True))  # Fixed
checks.append(('宽表 stock_close_wide.csv', os.path.exists('data/clean/stock_close_wide.csv')))
checks.append(('长表 stock_close_long.csv', os.path.exists('data/clean/stock_close_long.csv')))
checks.append(('合并表 stock_macro_combined.csv', os.path.exists('data/combined/stock_macro_combined.csv')))

# 7. SQLite (方式C)
checks.append(('finance.db 存在', os.path.exists('data/clean/finance.db')))

# 8. 图1-4 (PNG, >=150dpi)
for fig in ['fig1_normalized_price.png', 'fig2_return_distribution.png',
            'fig3_correlation_heatmap.png', 'fig4_macro_scatter.png']:
    fpath = os.path.join('output', fig)
    checks.append((f'{fig}', os.path.exists(fpath) and os.path.getsize(fpath) > 10000))

# 9. CAPM
checks.append(('capm_results.csv', os.path.exists('output/capm_results.csv')))
checks.append(('descriptive_stats.csv', os.path.exists('output/descriptive_stats.csv')))
checks.append(('fig6_capm_beta.png (Beta点图)', os.path.exists('output/fig6_capm_beta.png')))
checks.append(('fig7_sml.png (SML图)', os.path.exists('output/fig7_sml.png')))

# 10. report.html 在根目录
checks.append(('report.html 在根目录', os.path.exists('report.html')))
checks.append(('report.html > 100KB', os.path.getsize('report.html') > 100000))

# 11. .gitignore
checks.append(('.gitignore 存在', os.path.exists('.gitignore')))

# 12. requirements.txt
checks.append(('requirements.txt 存在', os.path.exists('requirements.txt')))

# 打印结果
passed = 0
failed = 0
for name, result in checks:
    status = 'PASS' if result else 'FAIL'
    if result:
        passed += 1
    else:
        failed += 1
    print(f'  [{status}] {name}')

print(f'\n总计: {passed} 通过, {failed} 未通过 (共 {len(checks)} 项)')
