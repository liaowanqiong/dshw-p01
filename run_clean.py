import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

nb_path = '02_clean.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=300, kernel_name='python3', allow_errors=True)
ep.preprocess(nb, {'metadata': {'path': '.'}})

error_count = 0
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and cell.outputs:
        for output in cell.outputs:
            if output.output_type == 'error':
                error_count += 1
                print(f'ERROR in cell {i}: {output.ename}: {output.evalue}')

with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f'02_clean.ipynb executed: {error_count} errors')
