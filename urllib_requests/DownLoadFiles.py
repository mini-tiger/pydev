#coding=utf-8
from os.path import basename
from urlparse import urlsplit
import sys
import os,logging
import time
import urllib2
import csv,ConfigParser
import gzip
import string
 

class DownLoadFiles(): 
    def __init__(self):
        #self.home = os.getcwd()       
        #下载列表文件路径      
        #self.configFile = os.path.join(os.getcwd() ,'UrlList.csv') 
        #文件下载目录      
        #self.downLoadDir = 'E:\\DownLoadFiles_' + time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))    
        
        root = os.path.dirname(__file__)
        configfile = os.path.join(root,'config.ini')
        cf = ConfigParser.ConfigParser() 
        cf.read(configfile)
        self.downLoadDir=cf.get(main,download_Dir) 
        self.logdir=cf.get(main,logDir)
        self.active = cf.get(main,active) 

    def url2name(self, url):
        return basename(urlsplit(url)[2])    
    
    def downloadFile(self, url, localFileName = None): 
        #cityDir = os.path.join(self.downLoadDir, city)
        if not os.path.isdir(self.downLoadDir):
            os.makedirs(self.downLoadDir)
        os.chdir(self.downLoadDir)
        localName = self.url2name(url)
        req = urllib2.Request(url)
        r = urllib2.urlopen(req)
        if r.info().has_key('Content-Disposition'):
            localName = r.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        elif r.url != url:
            localName = url2name(r.url)
        if localFileName:
            localName = localFileName        
        f = open(localName, 'wb')
        f.write(r.read())
        f.close()        
        return localName

        
    def run(self):
        publishFileNameList = []
        os.chdir(self.home)        
        if os.path.exists(self.configFile):
            with open(self.configFile, 'rb') as file:
                _reader = csv.DictReader(file)
                for row in _reader:
                    #下载发布文件
                    try:     
                        originalFileName = self.downloadFile(row['Url'].strip(), localFileName = None)
                        publishFileNameList.append(originalFileName)
                    except Exception as e :
#                        logger.error('程序下载文件错误，url='+row['Url'].strip())
                        import traceback
                        traceback.print_exc()
                    
            file.close()
            print 'downlad publish files successfully'
            
    
if __name__ == '__main__':
    test = DownLoadFiles()
    test.run()
    
