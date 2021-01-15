import multiprocessing
from multiprocessing.managers import BaseManager
import threading

# 锁可以通过global也可以在Process中传无所谓
share_lock = threading.Lock()

# 定义一个要共享实例化对象的类
class Test():
    def __init__(self):
        self.test_list = ["start flag"]

    def test_function(self,arg):
        self.test_list.append(arg)

    def print_test_list(self):
        for item in self.test_list:
            print(f"{item}")

def sub_process(process_name,obj):
    global share_lock
    share_lock.acquire()
    obj.test_function(f"{process_name}")
    share_lock.release()
    obj.print_test_list()
    pass

def main_process():
    # 如果是想注册open方法这样操作
    # manager = BaseManager()
    # # 一定要在start前注册，不然就注册无效
    # manager.register('open', open)
    # manager.start()
    # obj = manager.open("1.txt","a")

    # 为了更加直接我们直接以一个Test类的实例化对象来演示
    manager = BaseManager()
    # 一定要在start前注册，不然就注册无效
    manager.register('Test', Test)
    manager.start()
    obj = manager.Test()

    process_list = []
    # 创建进程1
    process_name = "process 1"
    tmp_process = multiprocessing.Process(target=sub_process,args=(process_name,obj))
    process_list.append(tmp_process)
    # 创建进程2
    process_name = "process 2"
    tmp_process = multiprocessing.Process(target=sub_process, args=(process_name,obj))
    process_list.append(tmp_process)
    # 启动所有进程
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()


if __name__ == "__main__":
    main_process()