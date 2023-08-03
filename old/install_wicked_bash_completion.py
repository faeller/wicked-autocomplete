#!/usr/bin/env python3

import os
import argparse

# Create an ArgumentParser instance
parser = argparse.ArgumentParser(description='Install Bash autocompletion for wicked commands')

parser.add_argument('-o', '--output', help='Output file path', default='/etc/bash_completion.d/wicked')

# Parse the command-line arguments
args = parser.parse_args()

# Define the hardcoded bash completion script
script = """
_wicked_autocomplete()
{
    local cur prev options
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    commands="ifup ifdown ifreload ifstatus ifcheck show-config convert show-xml xpath getnames duid iaid arp ethtool"
    options="--config --log-level --log-target --debug --root-directory --dry-run --systemd --transient --ifconfig"

    case "${prev}" in
        wicked)
            COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            return 0
            ;;
        *)
            COMPREPLY=( $(compgen -W "${options}" -- ${cur}) )
            return 0
            ;;
    esac
}

complete -F _wicked_autocomplete wicked
"""

# Ensure the directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Write the script to the specified output file
with open(args.output, 'w') as f:
    f.write(script)
