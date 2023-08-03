#!/usr/bin/env python3
import argparse
import subprocess
import os
import re

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        raise Exception(error.decode('utf-8'))
    return output.decode('utf-8')

def parse_wicked_options_from_help_output(help_output):
    match = re.search(r'Options:\n(.*?)\nCommands:', help_output, re.DOTALL)
    if match:
        options_text = match.group(1)
        options_lines = options_text.split('\n')
        options = [line.strip().split()[0] for line in options_lines if line.strip()]
        return options
    else:
        raise Exception("Unable to find 'Options:' in wicked help output")

def parse_wicked_commands_from_help_output(help_output):
    match = re.search(r'Commands:\n(.*?)(\n\n|$)', help_output, re.DOTALL)
    if match:
        commands_text = match.group(1)
        commands_lines = commands_text.split('\n')
        commands = [line.strip().split()[0] for line in commands_lines if line.strip()]
        return commands
    else:
        raise Exception("Unable to find 'Commands:' in wicked help output")

def write_bash_completion_script(output_file, options, commands):
    with open(output_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("_wicked_autocomplete()\n")
        f.write("{\n")
        f.write("    local cur prev\n")
        f.write("    COMPREPLY=()\n")
        f.write("    cur=\"${COMP_WORDS[COMP_CWORD]}\"\n")
        f.write("    prev=\"${COMP_WORDS[COMP_CWORD-1]}\"\n")
        f.write(f"    commands=\"{' '.join(commands)}\"\n")
        f.write(f"    options=\"{' '.join(options)}\"\n") 
        f.write("\n")
        f.write("    case \"${prev}\" in\n")
        f.write("        wicked)\n")
        f.write("            COMPREPLY=( $(compgen -W \"${commands}\" -- ${cur}) )\n")
        f.write("            return 0\n")
        f.write("            ;;\n")
        f.write("        *)\n")
        f.write("            COMPREPLY=( $(compgen -W \"${options}\" -- ${cur}) )\n")
        f.write("            return 0\n")
        f.write("            ;;\n")
        f.write("    esac\n")
        f.write("}\n")
        f.write("\n")
        f.write("complete -F _wicked_autocomplete wicked\n")

    # Set the execute permission for the generated script
    os.chmod(output_file, os.stat(output_file).st_mode | 0o111)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a bash completion script for wicked.')
    parser.add_argument('--output', type=str, required=False, default='/etc/bash_completion.d/wicked', help='The output file to write the bash completion script to.')

    args = parser.parse_args()

    if os.getuid() != 0:
        print("Please run as root")
        exit(1)

    wicked_help_output = execute_command("sudo wicked --help")
    options = parse_wicked_options_from_help_output(wicked_help_output)
    commands = parse_wicked_commands_from_help_output(wicked_help_output)

    write_bash_completion_script(args.output, options, commands)
    print(f"Autocompletion script written to: {args.output}")
