from celery import Celery



brokers = 'redis://10.70.61.97:6379/1'   ##..redis...DB.....0.
backend = 'redis://10.70.61.97:6379/2'

app = Celery('tasks', broker=brokers, backend=backend)
app.conf.update(CELERY_ENABLE_UTC=True)

from kombu import Queue

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='default'),
    Queue("queue_add", routing_key='queue_add'),
    Queue('queue_sum', routing_key='queue_sum'),
)


app.conf.task_routes = {
    'add':{'queue':'queue_add', 'routing_key':'queue_add'},
    'sum':{'queue':'queue_sum', 'routing_key':'queue_sum'},
}

@app.task
def add(x, y):
    return x + y
@app.task
def reduce(x, y):
    return x - y





@app.task
def other(x, y):
    return x * y

