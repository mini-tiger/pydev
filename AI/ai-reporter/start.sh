#!/bin/bash
# shellcheck disable=SC2034
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
echo $PYTHONPATH
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER
[ -z "$RUN_TYPE" ] && export RUN_TYPE=portal
[ -z "$WORD_HOST_WIN" ] && export WORD_HOST_WIN=59.151.19.81:5000

# docker env
[ -z "$DOWNLOAD_URL" ] && export DOWNLOAD_URL=http://120.133.63.166:5004/attachment/download/
[ -z "$OPENAI_API_BASE" ] && export OPENAI_API_BASE=http://120.133.75.252:28002/v1
[ -z "$GPUOS_PLATFORM_URL" ] && export GPUOS_PLATFORM_URL=http://120.133.83.136:11017/api/v1/chat/completions
[ -z "$OUTLINE_MODEL_TYPE" ] && export OUTLINE_MODEL_TYPE=model_3
[ -z "$VECTOR_OPEN" ] && export VECTOR_OPEN=1
[ -z "$GPUOS_PLATFORM" ] && export GPUOS_PLATFORM=1
[ -z "$LANGCHAIN_RAG" ] && export LANGCHAIN_RAG=0

pushd $SHELL_FOLDER/webapi/app || exit
[ -z "$FLASK_PORT" ] && export FLASK_PORT=5004

python main.py
popd || exit