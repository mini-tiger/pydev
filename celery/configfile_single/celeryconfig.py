from kombu import Exchange,Queue

BROKER_URL = "redis://10.70.61.97:6379/1" 
CELERY_RESULT_BACKEND = "redis://10.70.61.97:6379/2"

CELERY_QUEUES = (
#Queue("default",Exchange("default"),routing_key="default"),
Queue("for_task_A",Exchange("for_task_A"),routing_key="task_a"),
Queue("for_task_B",Exchange("for_task_B"),routing_key="task_a") 
)
    
CELERY_ROUTES = {
    'tasks.r_sql':{"queue":"for_task_A","routing_key":"task_a"},
    'tasks.taskB':{"queue":"for_task_B","routing_key":"task_b"}
}
