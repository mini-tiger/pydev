#!/bin/bash
# shellcheck disable=SC2034
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
echo $PYTHONPATH
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER
export RUN_TYPE=prod
#export bertclassifymodelurl=http://127.0.0.1:8000/search/reportClassify
export DOWNLOAD_URL=http://120.133.63.166:5004/attachment/download/
export OPENAI_API_BASE=http://120.133.63.162:33382/v1,http://120.133.63.162:33382/v1
export GPUOS_PLATFORM_URL=http://120.133.83.136:11017/api/v1/chat/completions
export OUTLINE_MODEL_TYPE=model_3
export VECTOR_OPEN=1
export GPUOS_PLATFORM=1
export LANGCHAIN_RAG=0
pushd $SHELL_FOLDER/webapi/app || exit
export FLASK_PORT=5004
python main.py
popd || exit