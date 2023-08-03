#!/bin/bash

_wicked_autocomplete() {
    local current_command=${COMP_LINE}
    local suggestions=$(python3 /usr/local/bin/wicked_autocompleter.py ${current_command})
    COMPREPLY=($suggestions)
}

complete -F _wicked_autocomplete wicked
