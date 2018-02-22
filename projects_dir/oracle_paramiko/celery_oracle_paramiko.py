from celery import Celery

brokers = 'redis://10.70.61.97:6379/1'   ##..redis...DB.....0.
backend = 'redis://10.70.61.97:6379/2'

app = Celery('tasks', broker=brokers, backend=backend)

@app.task
def add(x, y):
    return x + y
@app.task
def xsum(numbers):
    return sum(numbers)