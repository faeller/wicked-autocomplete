#!/usr/bin/env python3

import shutil
import os

# Path to the Bash script for wicked autocompletion (relative or absolute)
bash_script_path = './wicked-autocomplete.sh'
# Get the absolute path
bash_script_path = os.path.realpath(bash_script_path)

# Path to the autocompleter binary
autocompleter_binary_path = './wicked-autocomplete'
# Get the absolute path
autocompleter_binary_path = os.path.realpath(autocompleter_binary_path)

# Target paths to copy the Bash and Python scripts
target_bash_path = '/usr/share/bash-completion/completions/wicked'
target_binary_path = '/usr/local/bin/wicked-autocomplete'

# Copy the Bash script to the target location
shutil.copy(bash_script_path, target_bash_path)
os.chmod(target_bash_path, 0o755)

# Copy the Python script to the target location
shutil.copy(autocompleter_binary_path, target_binary_path)
os.chmod(target_binary_path, 0o755)

print("Wicked autocompletion installed successfully!")
