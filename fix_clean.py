import json

nb_path = '02_clean.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and replace cell-14 (outlier detection)
new_cell14_source = [
    "print('='*60)\n",
    "print('2.6 离群值标注')\n",
    "print('='*60)\n",
    "\n",
    "# 作业要求: 计算日收益率，单日涨跌幅超±20%标为 is_extreme=True\n",
    "# 注意: 不删除离群值，仅标注\n",
    "outlier_summary = []\n",
    "for name, df in stock_dfs.items():\n",
    "    df['is_extreme'] = False\n",
    "    extreme_mask = df['daily_return'].abs() > 20  # 单日涨跌幅超±20%\n",
    "    df.loc[extreme_mask, 'is_extreme'] = True\n",
    "    n_extreme = extreme_mask.sum()\n",
    "    outlier_summary.append({\n",
    "        '股票': name,\n",
    "        '极端涨跌天数': int(n_extreme),\n",
    "        '占比': f'{n_extreme/len(df)*100:.2f}%',\n",
    "        '阈值': '±20%',\n",
    "        '处理方式': '标注，不删除'\n",
    "    })\n",
    "\n",
    "outlier_df = pd.DataFrame(outlier_summary)\n",
    "print(outlier_df.to_string(index=False))\n",
    "\n",
    "print('''\\n【说明】\n",
    "- 标注规则: 单日涨跌幅绝对值 > 20% 标记为 is_extreme=True\n",
    "- 处理方式: 仅标注不删除，保留原始数据完整性\n",
    "- 可能成因: 涨跌停板（主板±10%、创业板/科创板±20%）、\n",
    "  除权除息、公司重大事件公告、ST/退市风险警示等\n",
    "''')\n",
]

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if '2.6' in src and ('IQR' in src or '离群值' in src):
        cell['source'] = new_cell14_source
        print('Fixed cell-14: is_extreme column')
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved:', nb_path)
