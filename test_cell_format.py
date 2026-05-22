import json

def str_to_cell_source(code_str):
    """Convert a multi-line string to notebook cell source format (list of lines with newlines)."""
    lines = code_str.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        else:
            if line:  # Don't add empty last line
                result.append(line)
    return result

# Test
test_code = "import pandas as pd\nimport numpy as np\nprint('hello')"
src = str_to_cell_source(test_code)
print('Test:')
for s in src:
    print(repr(s))
print('Joined:', ''.join(src))
