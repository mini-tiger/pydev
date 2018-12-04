# -*- coding: UTF-8 -*-
import os,sys
# reload(sys)
# sys.setdefaultencoding('gbk')
import smtplib,datetime,os
from email.mime.text import MIMEText
from email.Header import Header

def mail_send(data):

    dt=datetime.datetime.now()
    zuo = dt - datetime.timedelta(days=1)
    zuotian = zuo.strftime('%Y%m%d')

    print data.get('content')
    txt="<html><body></body></html><font size='6' color='red'>"+data.get('content')+"</font>"
    msg=MIMEText(txt,_subtype='html',_charset='GBK')

    # sender = 'monitor@palmcity.cn'
    # tolist = ['monitor@palmcity.cn']   ##·¢ËÍ¶àÈË
    # smtpserver = 'smtp.ym.163.com'
    # username = 'monitor@palmcity.cn'
    # password = 'palmc2013#$%'

    sender = '61566027@163.com'
    tolist = []
    if data.get("tos"):
        tolist.append(str(data.get("tos")))

    # smtpserver = 'smtp.163.com'
    username = '61566027@163.com'
    # password = '123.com'
    password = "Taojun319" # 授权码


    ##¶¨ÒåÓÊ¼þ±êÌâ
    # msg['Subject'] = Header("报警 "+' '+str(datetime.date.today()),'UTF-8')
    msg['Subject'] = Header(data.get("subject"), 'UTF-8')
    ##ÓÊ¼þ·¢ËÍÉèÖÃ
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    # smtp.connect('smtp.ym.163.com')
    smtp.login(username, password)
    ##SMTP.sendmail(·¢¼þÈË£¬ÊÕÐÅÈË£¬ÄÚÈÝ)
    for to in tolist:
        smtp.sendmail(sender, [to], msg.as_string())
    smtp.quit()

