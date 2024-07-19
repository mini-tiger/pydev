#!/bin/bash
export ZZ=1
#export RECREATE_TABLE=True
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
echo $PYTHONPATH
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER
python Chain3_prompt.py