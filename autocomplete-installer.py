#!/usr/bin/env python3

import shutil
import os

# Path to the Bash script for wicked autocompletion (relative or absolute)
bash_script_path = './wicked-autocomplete.sh'
# Get the absolute path
bash_script_path = os.path.realpath(bash_script_path)

# Path to the Python autocompleter script (relative or absolute)
python_script_path = './wicked-autocompleter.py'
# Get the absolute path
python_script_path = os.path.realpath(python_script_path)

# Target paths to copy the Bash and Python scripts
target_bash_path = '/usr/local/bin/wicked-autocomplete.sh'
target_python_path = '/usr/local/bin/wicked-autocompleter.py'

# Copy the Bash script to the target location
shutil.copy(bash_script_path, target_bash_path)
os.chmod(target_bash_path, 0o755)

# Copy the Python script to the target location
shutil.copy(python_script_path, target_python_path)
os.chmod(target_python_path, 0o755)

print("Wicked autocompletion installed successfully!")
