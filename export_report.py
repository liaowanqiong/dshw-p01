import nbformat, os
from nbconvert import HTMLExporter

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

html_exporter = HTMLExporter()
html_exporter.template_name = 'classic'
body, resources = html_exporter.from_notebook_node(nb)

out_path = os.path.join(os.getcwd(), 'output', 'report.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(body)

import shutil
shutil.copy(out_path, os.path.join(os.getcwd(), 'report.html'))

print('report.html exported:', os.path.getsize(out_path), 'bytes')
