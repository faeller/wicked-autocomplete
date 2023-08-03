import sys
import re

# Wicked main commands
WICKED_COMMANDS = [
    "ifup", "ifdown", "ifstatus", "ifcheck", "ifreload", "ifplugd", "ifmonitor",
    "show-config", "show-xml", "show-steady", "dhcp", "auto4", "auto6",
    "test", "fsm", "arp", "check", "sync", "leaseinfo", "rpc", "extensions", "logging",
    "compat", "hostname", "timers", "dbus", "client", "xml", "schema", "release-notes"
]

def get_interfaces_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if 'wicked ifstatus' in content:
                return get_interfaces_from_wicked(content)
            else:  # Parse 'ip a' output
                return get_interfaces_from_ip_a(content)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return ''

def get_interfaces_from_wicked(content: str) -> str:
    return ' '.join(line.split()[0] for line in content.strip().split('\n')[1:] if line.strip())

def get_interfaces_from_ip_a(content: str) -> str:
    return ' '.join(re.findall(r'^\d+:\s+([^:]+):', content, re.MULTILINE))

def get_interfaces() -> str:
    return get_interfaces_from_file('example-wicked-ifstatus.txt') or get_interfaces_from_file('example-ip-a-txt')

def get_wicked_autocomplete_suggestions(user_input: str) -> str:
    words = user_input.rstrip().split()
    if not words or words[0] != 'wicked':
        return ' '.join(WICKED_COMMANDS)
    if words[-1] in ['ifup', 'ifdown']:
        return get_interfaces()
    return ''

# Get the current command line input from the arguments
user_input = ' '.join(sys.argv[1:])
suggestions = get_wicked_autocomplete_suggestions(user_input)
print(suggestions)
