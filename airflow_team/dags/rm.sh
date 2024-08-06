#!/bin/bash

YYMMDD=$1

DONE_PATH=/home/sujin/code/playgogo/storage
DONE_PATH_FILE="${DONE_PATH}/_DONE"

if [ -e "${DONE_PATH_FILE}" ]; then
    figlet "Let's move on"
    exit 0
else
    echo "I'll be back => ${DONE_PATH_FILE}"
    exit 1
fi
