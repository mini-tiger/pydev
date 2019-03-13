# coding:utf-8
import threading
import time

counter = 0
# 只是定义一个锁,并不是给资源加锁,你可以定义多个锁,像下两行代码,当你需要占用这个资源时，任何一个锁都可以锁这个资源
counter_lock = threading.Lock()
counter_lock2 = threading.Lock()
counter_lock3 = threading.Lock()


# 可以使用上边三个锁的任何一个来锁定资源

# global counter,counter_lock # 多线程是共享资源的，使用全局变量


class MyThread1(threading.Thread):  # 使用类定义thread，继承threading.Thread

	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = "Thread-" + str(name)

	def run(self):  # run函数必须实现
		global counter, counter_lock  # 多线程是共享资源的，使用全局变量
		# 当需要独占counter资源时，必须先锁定，这个锁可以是任意的一个锁，可以使用上边定义的3个锁中的任意一个
		try:
			if counter_lock.acquire():
				print('现在{}锁定状态'.format('是' if counter_lock.locked() else '不是'))
				counter += 1
				print("I am %s--%s, set counter:%s" % (self.__class__.__name__,self.name, counter))
				print('线程: {} ,运行结束'.format(self.name))

				# counter_lock.release()
		except Exception as e:
			print(e)
			counter_lock.release()
			# 使用完counter资源必须要将这个锁打开，让其他线程使用
		finally:
			print('-' * 50)
			counter_lock.release()  # 使用完counter资源必须要将这个锁打开，让其他线程使用


class MyThread2(threading.Thread):  # 使用类定义thread，继承threading.Thread

	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = "Thread-" + str(name)

	def run(self):  # run函数必须实现
		global counter, counter_lock  # 多线程是共享资源的，使用全局变量
		# 当需要独占counter资源时，必须先锁定，这个锁可以是任意的一个锁，可以使用上边定义的3个锁中的任意一个
		try:
			if counter_lock.acquire():
				print('现在{}锁定状态'.format('是' if counter_lock.locked() else '不是'))
				counter += 1
				print("I am %s--%s, set counter:%s" % (self.__class__.__name__,self.name, counter))
				print('线程: {} ,运行结束'.format(self.name))

				# counter_lock.release()
		except Exception as e:
			print(e)
			counter_lock.release()
			# 使用完counter资源必须要将这个锁打开，让其他线程使用
		finally:
			print('-' * 50)
			counter_lock.release()  # 使用完counter资源必须要将这个锁打开，让其他线程使用


if __name__ == "__main__":
	for i in range(1, 101):
		if i % 2 == 0:
			my_thread1 = MyThread1(i)
			my_thread1.start()
		else:
			my_thread2 = MyThread2(i)
			my_thread2.start()
