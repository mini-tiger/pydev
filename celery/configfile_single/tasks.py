from celery import Celery
from utils import SSHConnected
from utils import sql as oracle_sql

app = Celery()
app.config_from_object("celeryconfig")

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
def taskB(x,y,z):
     return x + y + z

@app.task
def add(x,y):
    return x + y
