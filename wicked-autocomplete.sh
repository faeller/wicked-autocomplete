#!/bin/bash

_wicked_autocomplete() {
    local current_command=${COMP_LINE}
    local suggestions=$(/usr/local/bin/wicked_autocomplete ${current_command})
    COMPREPLY=($suggestions)
}

complete -F _wicked_autocomplete wicked
