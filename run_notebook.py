import nbformat, os
from nbconvert.preprocessors import ExecutePreprocessor

nb_path = '03_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
print('开始运行 notebook...')
ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print('Notebook 运行完成，已保存')
