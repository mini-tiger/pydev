# coding:utf-8
'''
celery worker -A celery_oracle_paramiko --loglevel=info -E -Q for_task_A
'''
from celery import Celery,platforms
from utils import SSHConnected
from utils import sql as oracle_sql

from kombu import Queue,Exchange

brokers = 'redis://10.70.61.97:6379/1'
backend = 'redis://10.70.61.97:6379/2'

app = Celery(broker=brokers, backend=backend)
platforms.C_FORCE_ROOT = True
class config1():
	#BROKER_URL = "redis://10.70.61.97:6379/1"
	#CELERY_RESULT_BACKEND = "redis://10.70.61.97:6379/2"

	CELERY_QUEUES = (
        #Queue("default",Exchange("default"),routing_key="default"),
	Queue("for_task_A",Exchange("for_task_A"),routing_key="task_a"),
	Queue("for_task_B",Exchange("for_task_B"),routing_key="task_a")
	)

	CELERY_ROUTES = {
        'celery_oracle_paramiko.r_sql':{"queue":"for_task_A","routing_key":"task_a"},
        'tasks.taskB':{"queue":"for_task_B","routing_key":"task_b"}
	}
        #task_default_queue= 'default'
        #task_default_routing_key = 'default'
        #task_default_exchange_type = 'direct'
        #task_default_exchange = 'tasks'
        #worker_max_tasks_per_child = 20
	#task_default_queue= 'default'
	#task_default_routing_key = 'default'
	#task_default_exchange_type = 'direct'
	#task_default_exchange = 'tasks'
	#worker_max_tasks_per_child = 20
	CELERYD_MAX_TASKS_PER_CHILD = 20	
#	CELERY_default_queue = 'default' ,  ##默认的队列
	#CELERY_default_exchange = 'tasks', # 默认的交换机名字为tasks
	#CELERY_default_exchange_type = 'direct' # 默认的交换类型是direct 直接匹配   topic可以模糊匹配 
	#CELERY_default_routing_key = 'default', # 默认的路由键是task.default，这个路由键符合上面的default队列

c=config1()
app.config_from_object(c)




#app.conf.task_queues = (
#    Queue('default', routing_key='default'),
#    Queue("run_sql",  Exchange('run_sql', type='direct'),routing_key='queue_sql'), ## 模糊匹配 routing_key
#    Queue('run_ssh', routing_key='queue_ssh'),
#)


#app.conf.task_routes = {
#    'add':{'queue':'default', 'routing_key':'default'},
#    'r_sql':{'queue':'run_sql','routing_key':'queue_sql'},
#    'run_ssh':{'queue':'run_ssh', 'routing_key':'queue_ssh'},
#}

@app.task ##test
def add(x,y):
	return x+y

@app.task
def r_sql(ip,sid,sql):
	s=oracle_sql.util_sql(ip,"1521",sid)
	r=s.main()
	if r.get('error'):
		return r.get('error')
		exit(0)

	# r=s.exec_sql("select database_role from v$database")
	r=s.exec_sql(sql)
	try:
		if r.get('ret'):
			return r.get('sql_result')
		else:
			return r.get('error')
	# print s.exec_sql("select process, pid, status, client_process, client_pid from v$managed_standby")
	finally:
		s.close_session()
@app.task
def run_ssh():
	return 1
if __name__ == "__main__":
	app.start()
