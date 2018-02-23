# -*- coding: utf-8 -*-

import urllib, urllib2
import time, os, re
import traceback
import requests
import logging

if os.path.isfile('myapp.log'):
    os.remove("myapp.log")

logging.basicConfig(level=logging.DEBUG,
                format='[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='myapp.log',
                filemode='w')

class download(object):
    """docstring for ClassName"""

    def __init__(self):

        self.url = 'https://www.jiedaibao10g.com/10g/'
        self.url_source = 'https://www.jiedaibao10g.com'

        self.r = urllib2.Request(self.url)
        self.r.add_header('User-Agent', 'windows Internet')
        self.source_dir="g:\\10g"
        self.readed_url=[]
        self.downloaded_url=[]


    def request_read_url(self,url):
        try:
            r = requests.get(url,timeout=60)
            html= r.text.encode('utf-8')
            # print html
            html=html.split("\n")
            # print html
            return html
        except Exception as e:
            print e
            return e


    def read_url(self,url):
        try:

            r = urllib2.Request(url)
            r.add_header('User-Agent', 'windows Internet')
            response = urllib2.urlopen(r, timeout=30)
            html = response.read()
            html=html.split("\n")

            logging.debug('urilib2 read url: ' + url)
            return html


        except Exception as e:        
            print '错误提示'+ str(e)
            logging.debug( u'错误提示'+ str(e))
            print '使用request重试'
            logging.debug(u'使用request重试')
            logging.debug('request read url: ' + url)
            request_html=self.request_read_url(url)
            print request_html
            logging.debug('request html: ' + str(request_html))
            return request_html


            # print "重试一次"
            # if str(e).find('time out') != -1:  ##超时 重新一次
            #     print url
            #     html=self.read_url(url)
            #     return html


    def download_file(self,url,filename):

        if url in self.downloaded_url:
            print 'downloaded_url'
            return
        self.downloaded_url.append(url)

        print 'download url:' + url
        if url.find('jiedaibao10g') ==-1:

            if int(url.split('page=')[1]) not in self.url_two_page:  ##下一页链接

                print '不完整URL:' + url
                logging.debug(u'不完整URL:' + url)
                
                self.url_two_page.append(int(url.split('page=')[1]))
                url=self.url_source+url.split('http:')[1]
                print '重写URL:' + url
                logging.debug(u'重写URL:' + url)
                # print self.url_two_page
                self.read_url_four(url,filename)
            return

        # print url.split('/')[-1],url.split('/')


        file=os.path.join(os.getcwd(), url.split('/')[-1])
        print "file:  "+file,os.path.isfile(file)

        if not os.path.isfile(file):
            try:
                print url
                print file

                logging.debug(u'下载文件url : '+url)
                logging.debug(u'下载文件 : '+file.split('\\')[-1])

                r = urllib2.Request(url)
                r.add_header('User-Agent', 'windows Internet')

                f = urllib2.urlopen(r,timeout=30)
                with open(file, "wb") as code:
                   code.write(f.read())
            except Exception as e:
                print e
                print '下载错误 :' + str(e)+'重试下载'
                logging.debug(u'下载错误 :' + str(e)+u'重试下载')
                # traceback.print_exc()
                # if str(e).find('time out') != -1:  ##超时 重新一次
                    # r = urllib2.Request(url)
                    # r.add_header('User-Agent', 'windows Internet')
                    #
                    # f = urllib2.urlopen(r,timeout=30)
                    # with open(file, "wb") as code:
                    #    code.write(f.read())
                r = requests.get(url,timeout=60)

                with open(file, "wb") as code:
                    code.write(r.content)

        else:
            logging.debug('file exist :' + file.split('\\')[-1])
            return

    def read_url_four(self,url,filename):

        if url not in self.readed_url:
            html=self.read_url(url)
            self.readed_url.append(url)
        else:
            return
        # html=self.read_url(url)
        if html:
            for i in html:
                if (i.find('jpg') != -1 or i.find('png') != -1) and i.find('shield-ok-icon64-2.png') == -1 and \
                        i.find("//s.jiedaibao10g.com/qr/jiedaibao10g.com.png") == -1:
                    print "url source code four:"
                    logging.debug("url source code four:")
                    f = re.findall(r"(?<=href=\").+?(?=</a>)",i)
                    print f
                    for m in f:
                        m= m.split("\">")
                        # print m
                        # if i[1].find('上一级') == -1: ##不包括网页中上一级目录
                        url='http:'+m[0]
                        print url
                        logging.debug(url)
                        # self.read_url_four(url,i[1])
                        self.download_file(url,filename)

    def read_url_three(self,url):  ##第三页 是点击图片列表后的 图片显示
        # self.readed_url.append(url)
        # if url not in self.readed_url:
        #     html=self.read_url(url)
        # else:
        #     return
        html=self.read_url(url)
        if html:

            for i in html:
                if i.find('相片') != -1:
                    # print "url source code three:"
                    # logging.debug("url source code three:")
                    f = re.findall(r"(?<=href=\").+?(?=</a>)",i)
                    for i in f:
                        i= i.split("\">")
                        # print i
                        # if i[1].find('上一级') == -1: ##不包括网页中上一级目录
                        url=self.url_source+i[0]
                        logging.debug("url source code three:"+url)
                        print "url source code three:"+url
                        try:
                            self.read_url_four(url,i[1])
                        except Exception as e:
                            continue


    def read_url_two(self,url):  ##第二页 为 图片列表页
        self.url_two_page=[]

        html=self.read_url(url)

        if html:
            for i in html:
                if i.find('目录') != -1:
                    # print "url source code two:"+i
                    f = re.findall(r"(?<=href=\").+?(?=</a>)",i)
                    for i in f:

                        i= i.split("\">")
                        if i[1].find('上一级') == -1: ##不包括网页中上一级目录
                            self.make_dir(self.one_dir,i[1].decode('utf-8').encode('gbk'))
                            url=self.url_source+i[0]
                            logging.debug("read_url_two:  " + url)
                            # print url
                            os.chdir(os.path.join(self.one_dir,i[1].decode('utf-8').encode('gbk')))
                            self.read_url_three(url)

                            # print os.getcwd()
                            # self.url_dict_two.setdefault(i[1],i[0])


    def iter_url(self,url):

        print "--" * 80
        logging.debug("--" * 80)
        self.one_dir= os.getcwd()

        self.read_url_two(url)


    def make_dir(self,source_dir,dir):
        if not os.path.isdir(os.path.join(source_dir,dir)):
            os.makedirs(os.path.join(source_dir,dir))
        return


    def fusion_iter(self):
        for i in self.url_dict: ##主页遍历
            logging.debug(u"当前目录:  " + str(i).decode('utf-8'))
            logging.debug(u"当前URL:  " + self.url_dict[i])
            self.make_dir(self.source_dir,i.decode('utf-8').encode('gbk'))
            os.chdir(os.path.join(self.source_dir,i.decode('utf-8')))
            # print self.source_dir
            # print type(i)
            # print i.decode('utf-8')
            # print os.getcwd()
            self.iter_url(self.url_source+self.url_dict[i])



    def main(self):

        response = urllib2.urlopen(self.r, timeout=60)
        main_html = response.read()

        # print main_html
        # print '---------------------------------------------------'
        self.url_dict={}
        main_html_list = main_html.split('\n')

        for i in main_html_list:

            if i.find('目录') != -1:
                print "url source code:"+i
                logging.debug("url source code:"+i)
                # for a in  i.split('href="'):
                #     print a

                # p = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" , i)
                f = re.findall(r"(?<=href=\").+?(?=</a>)",i)
                # for i in p:
                #     print i
                for i in f:
                    i= i.split("\">")
                    self.url_dict.setdefault(i[1],i[0])

        self.fusion_iter()

if __name__ == "__main__":
    dd = download()

    # print "开始读取配置文件"
    dd.main()
