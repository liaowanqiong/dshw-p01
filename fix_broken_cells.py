import json

def str_to_src(code_str):
    """Convert multi-line string to notebook cell source format."""
    lines = code_str.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        else:
            if line:
                result.append(line)
    return result

with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Check broken cells and fix them
# The fix_all_chart_styles.py used .split('\n') which removes newlines
# We need to add newlines back

for cell in nb['cells']:
    cid = cell.get('id', '')
    if cid not in ('c1', 'c6', 'c7', 'c8', 'c9', 'c10', 'c16'):
        continue

    src = cell['source']
    if isinstance(src, list):
        # Check if first element has a newline
        if src and '\n' not in src[0] and len(src) == 1:
            # All code is in one line, need to split and add newlines
            code = src[0]
            cell['source'] = str_to_src(code)
            print('Fixed cell', cid, ':', len(code), 'chars ->', len(cell['source']), 'lines')
        elif src and '\n' not in src[0]:
            # Multiple elements but none have newlines - lines are glued
            # Join all, then re-split
            code = ''.join(src)
            cell['source'] = str_to_src(code)
            print('Re-split cell', cid, ':', len(code), 'chars ->', len(cell['source']), 'lines')
        else:
            # Already correct format
            print('Cell', cid, ': OK format')
    else:
        # string format, convert to list
        cell['source'] = str_to_src(str(src))
        print('Converted cell', cid, 'from str to list')

with open('03_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('\nNotebook saved. Verifying...')
# Verify
with open('03_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb2 = json.load(f)

for cell in nb2['cells']:
    cid = cell.get('id', '')
    if cid in ('c1', 'c6', 'c7', 'c8', 'c9', 'c10', 'c16'):
        src = cell['source']
        if isinstance(src, list) and src and '\n' in src[0]:
            print(cid + ': VERIFIED OK')
        elif isinstance(src, list) and len(src) > 1:
            # Check if it looks correct
            joined = ''.join(src)
            if 'import pandas' in joined[:50]:
                print(cid + ': looks OK (multi-line)')
            else:
                print(cid + ': WARNING - check manually')
        else:
            print(cid + ': WARNING - unexpected format')
