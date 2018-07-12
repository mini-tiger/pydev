from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
import time
## http://apscheduler.readthedocs.io/en/latest/userguide.html

## http://www.mamicode.com/info-detail-1846427.html


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler()

# .. do something else here, maybe add jobs etc.

scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')


def func1(a,b,l):
	print a,b,l

job1 = scheduler.add_job(func1, 'interval', seconds=1, args=['a','b',[1,2,3]],id="test")
scheduler.start()
print scheduler.get_jobs()
time.sleep(10)
job1.remove()  ## scheduler.remove_job('test')
scheduler.shutdown(wait=False)
print dir(scheduler)

# #循环任务示例
# scheduler.add_job(job1, ‘interval‘, seconds=5, args=(‘循环‘,), id=‘test_job1‘)
# #定时任务示例
# scheduler.add_job(job1, ‘cron‘, second=‘*/5‘, args=(‘定时‘,), id=‘test_job2‘)
# #一次性任务示例
# scheduler.add_job(job1, next_run_time=(datetime.datetime.now() + datetime.timedelta(seconds=10)), args=(‘一次‘,), id=‘test_job3‘)
# ‘‘‘
# 传递参数的方式有元组(tuple)、列表(list)、字典(dict)
# 注意：不过需要注意采用元组传递参数时后边需要多加一个逗号
# ‘‘‘
# #基于list
# scheduler.add_job(job2, ‘interval‘, seconds=5, args=[‘a‘,‘b‘,‘list‘], id=‘test_job4‘)
# #基于tuple
# scheduler.add_job(job2, ‘interval‘, seconds=5, args=(‘a‘,‘b‘,‘tuple‘,), id=‘test_job5‘)
# #基于dict
# scheduler.add_job(job3, ‘interval‘, seconds=5, kwargs={‘f‘:‘dict‘, ‘a‘:1,‘b‘:2}, id=‘test_job7‘)



# 事件监听，任务完成，任务退出等事件
from apscheduler.events import (EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_ALL_JOBS_REMOVED,
                                EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_SUBMITTED,
                                EVENT_JOB_MAX_INSTANCES, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_ALL)
scheduler.add_listener(event_listener, EVENT_ALL)
def event_listener(ev):
    msg = None
    if ev.code == EVENT_SCHEDULER_STARTED:
        msg = 'The scheduler was started.'
    if ev.code == EVENT_SCHEDULER_SHUTDOWN:
        msg = 'The scheduler was shut down.'
    if ev.code == EVENT_ALL_JOBS_REMOVED:
        msg = 'All jobs were removed from either all job stores or one particular job store.'
    if ev.code == EVENT_JOB_ADDED:
        msg = 'A job was added to a job store, job_id: %s' % (ev.job_id)
    if ev.code == EVENT_JOB_REMOVED:
        msg = 'A job was removed from a job store, job_id: %s' % (ev.job_id)
    if ev.code == EVENT_JOB_SUBMITTED:
        msg = 'A job was submitted to its executor to be run, job_id: %s' % (ev.job_id)
    elif ev.code == EVENT_JOB_MAX_INSTANCES:
        msg = 'reached maximum of running instances, job_id: %s' % (ev.job_id)
    if ev.code == EVENT_JOB_EXECUTED:
        msg = 'A job was executed successfully, job_id: %s' % (ev.job_id)
    if ev.code == EVENT_JOB_ERROR:
        msg = ev.traceback
    elif ev.code == EVENT_JOB_MISSED:
        msg = 'Missed job, job_id: %s, schedule_run_time: %s' % (ev.job_id, ev.scheduled_run_time)
    if msg:
        LOG.debug('JOB: %s' % msg)