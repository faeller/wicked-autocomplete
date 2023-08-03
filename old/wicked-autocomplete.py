#!/usr/bin/env python3

import difflib

# List of commands and options
commands_and_options = [
    'ifup', 'ifdown', 'ifreload', 'ifstatus', 'ifcheck', 'show-config', 'convert',
    'show-xml', 'xpath', 'getnames', 'duid', 'iaid', 'arp', 'ethtool', '--config',
    '--log-level', '--log-target', '--debug', '--root-directory', '--dry-run',
    '--systemd', '--transient', '--ifconfig'
]

def autocomplete(user_input):
    """
    Return a list of closest matches to user_input from commands_and_options.
    """
    return difflib.get_close_matches(user_input, commands_and_options)

def cli():
    """
    Simple command line interface that suggests commands or options as the user types.
    """
    try:
        while True:
            user_input = input("Enter a command or option: ")
            matches = autocomplete(user_input)
            if matches:
                print("Did you mean one of these?")
                for match in matches:
                    print('-', match)
            else:
                print("No matches found.")
    except KeyboardInterrupt:
        print("\nInterrupted by user")

if __name__ == "__main__":
    cli()