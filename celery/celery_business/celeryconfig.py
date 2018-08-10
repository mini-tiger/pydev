#coding=utf-8
from kombu import Exchange,Queue

BROKER_URL = "redis://192.168.43.11:6379/16" 
CELERY_RESULT_BACKEND = "redis://192.168.43.11:6379/17"
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_CONCURRENCY = 20  # 并发worker数
CELERYD_LOG_FILE =  "/root/logs/celery.log" # log路径
CELERYBEAT_LOG_FILE = "/root/logs/beat.log" # beat log路径
CELERYD_USER = 'celery'
CELERYD_GROUP = 'celery'
CELERYD_OPTS="--concurrency=8"
CELERYD_LOG_FILE="log/%n%I.log"

CELERY_QUEUES = (
Queue("default",Exchange("default"),routing_key="default"),
Queue("upload_file_ssh",Exchange("upload_file_ssh"),routing_key="upload_file_ssh"),
#Queue("for_task_B",Exchange("for_task_B"),routing_key="task_a") 
)
    
CELERY_ROUTES = {
    'tasks.upload_file_ssh':{"queue":"upload_file_ssh","routing_key":"upload_file_ssh"},
#    'tasks.taskB':{"queue":"for_task_B","routing_key":"task_b"}
}
