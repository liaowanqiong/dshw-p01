import nbformat
from nbconvert import HTMLExporter
import os

os.makedirs('output', exist_ok=True)

nb_path = '03_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

html_exporter = HTMLExporter()
html_exporter.exclude_input = False
html_exporter.exclude_output_prompt = True
html_exporter.exclude_input_prompt = True

(body, resources) = html_exporter.from_notebook_node(nb)

# Wrap with styling for better display
full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>03 分析与可视化 - 廖婉琼 (25210178)</title>
<style>
body {{
    font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #fafafa;
    line-height: 1.6;
}}
.container {{
    background: white;
    padding: 30px 40px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
h2 {{ color: #2980b9; margin-top: 30px; }}
h3 {{ color: #34495e; }}
pre {{
    background: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 13px;
    border-left: 4px solid #3498db;
}}
code {{
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
}}
img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    margin: 10px 0;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}}
th {{
    background: #3498db;
    color: white;
}}
tr:nth-child(even) {{ background: #f9f9f9; }}
.output_stream, .output_text {{
    white-space: pre-wrap;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    color: #333;
}}
</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>
"""

# Save to both output/ and project root
output_path = os.path.join('output', 'report.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f'Output: {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)')

root_path = 'report.html'
with open(root_path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f'Root: {root_path} ({os.path.getsize(root_path)/1024:.1f} KB)')
