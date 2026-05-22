"""Replace all remaining stock_colors references with stock_unique_colors."""
import json

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed = 0
for cell in nb['cells']:
    src_lines = cell.get('source', [])
    full_src = ''.join(src_lines)

    if 'stock_colors' in full_src and 'stock_unique_colors' not in full_src:
        # Replace stock_colors with stock_unique_colors
        new_lines = []
        for line in src_lines:
            new_lines.append(line.replace('stock_colors', 'stock_unique_colors'))
        cell['source'] = new_lines
        fixed += 1
        print(f"Fixed cell {cell.get('id', '?')}: replaced stock_colors -> stock_unique_colors")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\nTotal cells fixed: {fixed}")
