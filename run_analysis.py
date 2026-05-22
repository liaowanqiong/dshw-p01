import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import traceback

nb_path = '03_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)

try:
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    print('Notebook executed successfully!')

    error_count = 0
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and cell.outputs:
            for output in cell.outputs:
                if output.output_type == 'error':
                    error_count += 1
                    print(f'\nERROR in cell {i}: {output.ename}: {output.evalue}')
                    if output.traceback:
                        for line in output.traceback[-3:]:
                            print(f'  {line}')

    if error_count == 0:
        print('No errors found!')
    else:
        print(f'\nTotal errors: {error_count}')

    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f'Executed notebook saved to {nb_path}')

except Exception as e:
    print(f'Execution failed: {e}')
    traceback.print_exc()
