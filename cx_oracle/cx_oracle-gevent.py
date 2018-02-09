# coding:utf-8
from __future__ import print_function
import cx_Oracle
from cx_Oracle import DatabaseError


from time import time
from gevent import monkey
import gevent
from gevent.pool import Pool
from gevent.threadpool import ThreadPool
from gevent.queue import JoinableQueue, Empty

queue = JoinableQueue()
# STOP="stop"

monkey.patch_all()

class util_sql(object):
	def __init__(self, ip, port, SID):
		try:
			dsn = cx_Oracle.makedsn(ip, port, SID)

			self.conn = cx_Oracle.connect('sys', 'oracle', dsn, mode=cx_Oracle.SYSDBA)

			self.cursor = self.conn.cursor()
		except Exception as e:
			print (e)

	def close_session(self):
		self.conn.close()

	def exec_sql(self, sql):
		try:
			self.cursor.parse(sql)  # 验证sql

		except DatabaseError as e:

			return {'error':True,'detail':str(e)}

		try:
			result = self.cursor.execute(sql)

			if result != None:
				return {'result':result.fetchall()[0],'error':False}
			else:
				return {'result':None,'error':False }##DDL

		except  Exception as e:
			# print "sql : " + sql + "\n" + "exec error: " + str(e)
			return {'error':True,'detail':str(e)}



def util(n):
	s=util_sql("10.70.61.97","1521","XE")
	r=s.exec_sql(n)
	if not r.get('error',True):
		print (r,)
	else:
		print ('error: '+r['detail'])

	s.close_session()


def wheel():
    while True:
        try:
            print (gevent.getcurrent(),)
            n=queue.get(0)
            util(n)
        except Empty :    
        # except Exception as e:
            break



if __name__ == "__main__":


	start=time()
	pool=ThreadPool(5)
	print (pool.pid)
	sqls=["select database_role from v$database" for x in xrange(10)]

	for i in sqls:
	    queue.put(i)


	for i in xrange(10):
	    pool.spawn(wheel)


	pool.join()
	end=time()

	print (end-start)




