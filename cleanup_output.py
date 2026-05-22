import os, glob

output_dir = 'output'
# Remove old fig files that were from previous run
old_files = [
    'output/fig6_sml.png',       # replaced by fig7_sml.png
    'output/fig7_beta_vs_return.png',  # replaced by fig6_capm_beta.png
]

for f in old_files:
    if os.path.exists(f):
        os.remove(f)
        print(f'Removed: {f}')

print('\nCurrent output files:')
for f in sorted(os.listdir(output_dir)):
    size = os.path.getsize(os.path.join(output_dir, f))
    print(f'  {f} ({size/1024:.1f} KB)')
