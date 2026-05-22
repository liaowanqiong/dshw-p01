"""Run 03_analysis.ipynb and regenerate report.html."""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import os

nb_path = '03_analysis.ipynb'

# Execute notebook
print("Executing 03_analysis.ipynb ...")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
try:
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    print("Notebook executed successfully!")
except Exception as e:
    print(f"Error: {e}")

# Save executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

# Generate report.html
print("\nGenerating report.html ...")
result = subprocess.run(
    ['C:\\Users\\Admin1\\anaconda3\\Scripts\\jupyter.exe', 'nbconvert',
     '--to', 'html', '--output', 'report.html', nb_path],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print("stderr:", result.stderr)

# Copy to output/
import shutil
if os.path.exists('report.html'):
    shutil.copy2('report.html', 'output/report.html')
    print(f"\nreport.html copied to output/ ({os.path.getsize('report.html')/1024:.0f} KB)")
else:
    print("WARNING: report.html not generated!")
