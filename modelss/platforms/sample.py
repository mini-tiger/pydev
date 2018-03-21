# coding:utf-8

from __future__ import absolute_import,print_function
import platform

# help(platform)
# print platform.machine()
# print platform.node()
# print platform.system()
# print platform.uname()
# print platform.python_version()
# print platform.release()
# print platform.processor()
# print platform.platform()

print  (platform.platform())       #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
print  (platform.version())         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
print  (platform.architecture())    #获取操作系统的位数，('32bit', 'ELF')
print  (platform.machine())         #计算机类型，'i686'
print  (platform.node())            #计算机的网络名称，'XF654'
print  (platform.processor())       #计算机处理器信息，''i686'
print  (platform.uname())           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')

        #还可以获得计算机中python的一些信息：

print (platform.python_build())
print (platform.python_compiler())
print (platform.python_branch())
print (platform.python_implementation())
print (platform.python_revision())
print (platform.python_version())


import psutil  ##pip install psutil

print (help(psutil)) #http://psutil.readthedocs.io/en/latest/
print (psutil.Process())
print (psutil.disk_partitions())