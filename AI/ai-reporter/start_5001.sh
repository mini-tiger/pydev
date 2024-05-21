#!/bin/bash
# rsync -avzu /data/work/pydev/ai-reporter root@120.133.63.166:/home/taojun/backend_9001/ --exclude=.git --exclude=venv_* --exclude=__pycache__ --exclude=frontend --exclude=*.tar --exclude=*.log --exclude=/data/work/pydev/ai-reporter/webapi/app/attachments/
# shellcheck disable=SC2034
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
echo $PYTHONPATH
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER
export RUN_TYPE=prod
#export bertclassifymodelurl=http://127.0.0.1:8000/search/reportClassify
export DOWNLOAD_URL=http://120.133.63.166:5001/attachment/download/
export OPENAI_API_BASE=http://127.0.0.1:8001/v1,http://127.0.0.1:8002/v1,http://127.0.0.1:8000/v1,http://127.0.0.1:8003/v1
export WORD_HOST_WIN=59.151.19.81:5000
export OUTLINE_MODEL_TYPE=model_2
export VECTOR_OPEN=0
export GPUOS_PLATFORM=0
export LANGCHAIN_RAG=0
pushd $SHELL_FOLDER/webapi/app || exit
export FLASK_PORT=5001
python main.py
popd || exit