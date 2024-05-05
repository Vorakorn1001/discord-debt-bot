import subprocess

# Run pip freeze command to get installed packages and their versions
pip_freeze_output = subprocess.check_output(['pip', 'freeze']).decode('utf-8')

# Split the output into lines
filtered_packages = [package for package in pip_freeze_output.strip().split('\n') if "==" in package]

with open('requirements.txt', 'w') as f:
    f.write('\n'.join(filtered_packages))