#!/bin/bash
#export RECREATE_TABLE=True
export USE_GPU=True
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
echo $PYTHONPATH
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER
python Chain3_prompt.py