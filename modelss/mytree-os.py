# -*- coding: utf-8 -*-
import os


def getdir(dirsource, level=0):
	if not dirsource:
		dirsource = os.getcwd()
	dirlist = os.listdir(dirsource)
	level+=1
	for fd in dirlist:
		print '-' * level + fd
		fddir = os.path.join(dirsource, fd)
		if os.path.isdir(fddir):
			getdir(fddir, level)


getdir(dirsource=r'C:\Python27\Lib\site-packages')



