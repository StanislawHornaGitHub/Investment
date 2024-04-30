#!/bin/sh
### DESCRIPTION
# Script to set up logging settings.

### INPUTS
# None

### OUTPUTS
# None

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  30-Apr-2024
# Version:  1.0

# Date            Who                     What
#

LOG_PREFIX_PHRASE_NEW="log_line_prefix = '%m '"
LOG_PREFIX_PHRASE_DEFAULT="\#log_line_prefix = '%m \[%p\] '"

Main() {
    setLogPrefix
}

setLogPrefix() {
    sed -i "s/$LOG_PREFIX_PHRASE_DEFAULT/$LOG_PREFIX_PHRASE_NEW/" "$PGDATA/postgresql.conf"
}

Main
