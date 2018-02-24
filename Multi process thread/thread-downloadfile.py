#-*- coding:gbk -*-
import os,ConfigParser
import re,datetime,urllib,time
import threading,time,logging



        
    
class DownLoadFiles(object):
    def __init__(self):

        
        root = os.path.dirname(__file__)
        configfile = os.path.join(root,'config.ini')
        self.cf = ConfigParser.ConfigParser() 
        self.cf.read(configfile)

        downLoadDir=self.cf.get('main','download_Dir') 
        
        self.logdir=self.cf.get('main','logDir')
        self.logdir=os.path.join(root,self.logdir)
        self.log()
        
        self.active = self.cf.get('main','active').split(',')

        dt=datetime.datetime.now()
        riqi=dt.strftime('%Y%m%d')
        self.downLoadDir=os.path.join(downLoadDir,riqi)
        
        self.make_dir(self.downLoadDir)
        
        self.dict={}
        
    def log(self):   
        if not os.path.isdir(self.logdir):
            self.make_dir(self.logdir)
        
        logfile=os.path.join(self.logdir,'downfile.log')
        if not os.path.isfile(logfile):
            f = open(logfile, 'w')
            f.close()
        
        logging.basicConfig(level=logging.DEBUG,\
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
                        #datefmt='%Y-%m-%d %H:%M:%S',\
                        #filename=os.path.join(self.logdir,downfile.log),\   
                        filemode='a')
        
        from logging.handlers import RotatingFileHandler  ##���ع�����־ģ��
        #����һ��RotatingFileHandler��������౸��5����־�ļ���ÿ����־�ļ����10M ��������־������·���ļ�
        Rthandler = RotatingFileHandler(logfile,maxBytes=10*1024*1024,backupCount=5)
        Rthandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(levelname)-8s %(message)s')
        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler) 
        
    def make_dir(self,d):
        if not os.path.isdir(d):  ##����Ŀ¼
            os.makedirs(d)
        return
        
        
    def run(self):
        try:
            
            for self.i in self.active:
                self.init_download_list()
        except Exception as e:
            logging.error(str(e))
        
        return self.dict,self.downLoadDir

    def init_download_list(self):
        self.dict[self.i]={}
        self.regex_url('url_city')
        
        for city in self.cf.get(self.i,'citys').split(','):
            s=re.sub(self.regex,city,self.url_addr)
            self.dict[self.i][city]=s
            self.make_dir(os.path.join(self.downLoadDir,self.i,city)) ##��������Ŀ¼

        if self.cf.get(self.i,'inter'):  ##�����ļ��гǼ��Ƿ�Ϊ��
            self.regex_url('url_inter')
            for city in self.cf.get(self.i,'inter').split(','):
                s=re.sub(self.regex,city,self.url_addr)
                self.dict[self.i][city]=s
                self.make_dir(os.path.join(self.downLoadDir,self.i,city)) ##�����Ǽ�Ŀ¼
                
            
    def regex_url(self,u):
        self.url_addr=self.cf.get(self.i,u)  
        self.regex = re.compile(r"{}")
    

#{'base': {'1000': 'http://inter.palmcity.cn/portal/main.action?user=CJPLUST0&password=c984aed014aec7623a54f0591da07a85fd4b762d&citycode=1000&type=1&extension='}, \
#'word': {'1200': 'http://traffic.palmcity.cn/portal/main.action?user=PALMSTT11T0&password=4ac63cc33fce88f70cdf3af2d763320a23166cf5&citycode=1200&type=6&extension='}}


def now() :
    return str( time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ) )

                  
def thread_download(citycode,url,type):
    logging.info( '��ʼ���أ�'+ citycode+' type: ' + type + ' ��ʼʱ�� ' + now() )
    try:
        
        r = urllib.urlopen(url)
        code=r.getcode()
        if int(code) == 200 :
            if r.info().has_key('Content-Disposition'):
                localName = r.info()['Content-Disposition'].split('filename=')[1]
                localName = os.path.join(downLoadDir,type,citycode,localName)
                if not os.path.isfile(localName):
                    t=time.time()
                    urllib.urlretrieve(url,localName)
                    logging.info( '�ļ���' + localName + citycode+' type: ' + type + ' ʹ��ʱ��: ' + ('%.3f' % float(time.time() - t ) )+'��')
                else:
                    logging.info( '�ļ���' + localName + ' �ļ��Ѵ��� ' + citycode+' type: ' + type  )
            else:
                logging.error( 'HTTP����ͷ��������'+'Content-Disposition'+', citycode: ' +citycode+' type: ' + type  )
        else:
            logging.error( 'HTTP�����룺'+str(code)+', citycode: ' +citycode+' type: ' + type  )
    except Exception as e:
        logging.error(str(e))


def main(dict,downLoadDir):
    threadpool=[]
    for type in dict:
        for citycode,url in dict[type].items():
            
            th=threading.Thread(target= thread_download,args=(citycode,url,type))
            threadpool.append(th)

            
    for th in threadpool:
        #th.setDaemon(1)
        th.start()
        
#    for th in threadpool:
#        #threading.Thread.join( th )
#        th.join()
#            threading.Thread.join( th )
    print "all Done ", now()





        
        
if __name__ == '__main__':
    test = DownLoadFiles()
    dict,downLoadDir=test.run()
    main(dict,downLoadDir)
