#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: Sample.py
# Description: WXBizMsgCrypt 使用demo文件
#########################################################################
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import os, sys, time


class WeixinInterface:
    def __init__(self):
        ##些函数作用请看WEB模块文章
        self.app_root = os.path.dirname(__file__)

    # self.templates_root = os.path.join(self.app_root, 'templates')

    # self.render = web.template.render(self.templates_root)
    def GET(self):
        # 获取输入参数
        data = web.input()
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)  ##k加载wxcpt

        sVerifyMsgSig = data.msg_signature
        sVerifyTimeStamp = data.timestamp
        sVerifyNonce = data.nonce
        sVerifyEchoStr = data.echostr

        '''
           ret 代表wxcpt.VerifyURL 函数是否正确解析 正确是0，不正确非0,错误代码见ierror.py
        '''
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if (ret != 0):
            print "ERR: VerifyURL ret: " + str(ret)
            return
            '''
            返回，否则程序会死掉
            '''
        # sys.exit(1)
        else:
            return sEchoStr  ##回调验证 返回明文

    def TEXT(self):
        content = self.xml_tree.find("Content").text  ##找到XML中 的 提交过来的文本信息
        print "return text is" + content
        # touser= self.xml_tree.find("ToUserName").text
        # fromuser=self.xml_tree.find("FromUserName").text
        # msgtype=xml_tree.find("MsgType").text
        # AgentID=self.xml_tree.find("AgentID").text
        # msgid=self.xml_tree.find("MsgId").text  ##msgid 可以忽略
        createtime = str(int(time.time()))
        msg = "this is test"  ##要回复的内容
        ##以下 为回复消息时的 ，加密过程
        sRespData = "<xml><ToUserName><![CDATA[{0}]]></ToUserName><FromUserName><![CDATA[{1}]]></FromUserName><CreateTime>{2}</CreateTime><MsgType><![CDATA[{3}]]></MsgType><Content><![CDATA[{4}]]></Content><AgentID>{5}</AgentID></xml>".format(
            self.fromuser, self.touser, createtime, self.msgtype, msg, self.AgentID)
        # sRespData = "<xml><ToUserName><![CDATA[{0}]]></ToUserName><FromUserName><![CDATA[{1}]]></FromUserName><CreateTime>{2}</CreateTime><MsgType><![CDATA[{3}]]></MsgType><Content><![CDATA[{4}]]></Content><MsgId>{5}</MsgId><AgentID>{6}</AgentID></xml>".format(fromuser,touser,createtime,self.msgtype,msg,msgid,AgentID)
        ret, sEncryptMsg = self.wxcpt.EncryptMsg(sRespData, self.sReqNonce, self.sReqTimeStamp)
        if (ret != 0):
            print "ERR: EncryptMsg ret: " + str(ret)
            return
        # sys.exit(1)
        return sEncryptMsg

    def EVENT(self):
        msgtype = 'text'  ## 点击菜单事件，回复应该为 文本消息
        event = self.xml_tree.find("Event").text  ##找到XML中 的 提交过来的文本信息
        # touser= self.xml_tree.find("ToUserName").text
        # fromuser=self.xml_tree.find("FromUserName").text
        # msgtype=xml_tree.find("MsgType").text
        # AgentID=self.xml_tree.find("AgentID").text
        eventkey = self.xml_tree.find("EventKey").text
        createtime = str(int(time.time()))
        msg = "别瞎点：感谢陶钧对此次项目的极大支持"
        ##以下 为回复消息时的 ，加密过程
        sRespData = "<xml><ToUserName><![CDATA[{0}]]></ToUserName><FromUserName><![CDATA[{1}]]></FromUserName><CreateTime>{2}</CreateTime><MsgType><![CDATA[{3}]]></MsgType><Content><![CDATA[{4}]]></Content><AgentID>{5}</AgentID></xml>".format(
            self.fromuser, self.touser, createtime, msgtype, msg, self.AgentID)
        ret, sEncryptMsg = self.wxcpt.EncryptMsg(sRespData, self.sReqNonce, self.sReqTimeStamp)
        print sRespData
        if (ret != 0):
            print "ERR: EncryptMsg ret: " + str(ret)
            sys.exit(1)
        return sEncryptMsg

    def POST(self):
        sReqData = web.data()  ##获取 加密的XML
        data = web.input()  ##获取 参数
        print sToken, sEncodingAESKey, sCorpID
        self.wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)

        self.sReqMsgSig = data.msg_signature
        self.sReqTimeStamp = data.timestamp
        self.sReqNonce = data.nonce
        ret, sMsg = self.wxcpt.DecryptMsg(sReqData, self.sReqMsgSig, self.sReqTimeStamp, self.sReqNonce)
        if (ret != 0):
            print "ERR: DecryptMsg ret: " + str(ret)
            return
        # sys.exit(1)
        print sMsg
        self.xml_tree = ET.fromstring(sMsg)  ##sMsg  解密后的XML
        self.msgtype = self.xml_tree.find("MsgType").text
        self.touser = self.xml_tree.find("ToUserName").text
        self.fromuser = self.xml_tree.find("FromUserName").text
        self.AgentID = self.xml_tree.find("AgentID").text
        if self.msgtype == 'text':  ##通过类型判断 进入哪个函数
            return self.TEXT()
        elif self.msgtype == 'event':
            return self.EVENT()


if __name__ == "__main__":
    # 假设企业在公众平台上设置的参数如下
    sToken = "weixin"
    sEncodingAESKey = "BQptm8SueWbIj8z1NRPNSxdznzSAmRMiP54cKSmCsQh"
    sCorpID = "wx0a5e0ea42d34d2e1"
    urls = ("/weixin", "WeixinInterface")
    app = web.application(urls, globals())
    app.run()

    '''
     ------------使用示例一：验证回调URL---------------
     *企业开启回调模式时，企业号会向验证url发送一个get请求 
     假设点击验证时，企业收到类似请求：
     * GET /cgi-bin/wxpush?msg_signature=5c45ff5e21c57e6ad56bac8758b79b1d9ac89fd3&timestamp=1409659589&nonce=263014780&echostr=P9nAzCzyDtyTWESHep1vC5X9xho%2FqYX3Zpb4yKa9SKld1DsH3Iyt3tP3zNdtp%2B4RPcs8TgAE7OaBO%2BFZXvnaqQ%3D%3D 
     * HTTP/1.1 Host: qy.weixin.qq.com
 
     接收到该请求时，企业应	1.解析出Get请求的参数，包括消息体签名(msg_signature)，时间戳(timestamp)，随机数字串(nonce)以及公众平台推送过来的随机加密字符串(echostr),
     这一步注意作URL解码。
     2.验证消息体签名的正确性 
     3. 解密出echostr原文，将原文当作Get请求的response，返回给公众平台
     第2，3步可以用公众平台提供的库函数VerifyURL来实现。
    '''

    '''
     ------------使用示例二：对用户回复的消息解密---------------
     用户回复消息或者点击事件响应时，企业会收到回调消息，此消息是经过公众平台加密之后的密文以post形式发送给企业，密文格式请参考官方文档
     假设企业收到公众平台的回调消息如下：
     POST /cgi-bin/wxpush? msg_signature=477715d11cdb4164915debcba66cb864d751f3e6&timestamp=1409659813&nonce=1372623149 HTTP/1.1
     Host: qy.weixin.qq.com
     Content-Length: 613
     <xml>	<ToUserName><![CDATA[wx5823bf96d3bd56c7]]></ToUserName><Encrypt><![CDATA[RypEvHKD8QQKFhvQ6QleEB4J58tiPdvo+rtK1I9qca6aM/wvqnLSV5zEPeusUiX5L5X/0lWfrf0QADHHhGd3QczcdCUpj911L3vg3W/sYYvuJTs3TUUkSUXxaccAS0qhxchrRYt66wiSpGLYL42aM6A8dTT+6k4aSknmPj48kzJs8qLjvd4Xgpue06DOdnLxAUHzM6+kDZ+HMZfJYuR+LtwGc2hgf5gsijff0ekUNXZiqATP7PF5mZxZ3Izoun1s4zG4LUMnvw2r+KqCKIw+3IQH03v+BCA9nMELNqbSf6tiWSrXJB3LAVGUcallcrw8V2t9EL4EhzJWrQUax5wLVMNS0+rUPA3k22Ncx4XXZS9o0MBH27Bo6BpNelZpS+/uh9KsNlY6bHCmJU9p8g7m3fVKn28H3KDYA5Pl/T8Z1ptDAVe0lXdQ2YoyyH2uyPIGHBZZIs2pDBS8R07+qN+E7Q==]]></Encrypt>
     <AgentID><![CDATA[218]]></AgentID>
     </xml>
 
     企业收到post请求之后应该	1.解析出url上的参数，包括消息体签名(msg_signature)，时间戳(timestamp)以及随机数字串(nonce)
     2.验证消息体签名的正确性。	3.将post请求的数据进行xml解析，并将<Encrypt>标签的内容进行解密，解密出来的明文即是用户回复消息的明文，明文格式请参考官方文档
     第2，3步可以用公众平台提供的库函数DecryptMsg来实现。
    '''

    '''
     ------------使用示例三：企业回复用户消息的加密---------------
     企业被动回复用户的消息也需要进行加密，并且拼接成密文格式的xml串。
     假设企业需要回复用户的明文如下：
     <xml>
     <ToUserName><![CDATA[mycreate]]></ToUserName>
     <FromUserName><![CDATA[wx5823bf96d3bd56c7]]></FromUserName>
     <CreateTime>1348831860</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[this is a test]]></Content>
     <MsgId>1234567890123456</MsgId>
     <AgentID>128</AgentID>
     </xml>
 
     为了将此段明文回复给用户，企业应：	1.自己生成时间时间戳(timestamp),随机数字串(nonce)以便生成消息体签名，也可以直接用从公众平台的post url上解析出的对应值。
     2.将明文加密得到密文。	3.用密文，步骤1生成的timestamp,nonce和企业在公众平台设定的token生成消息体签名。	4.将密文，消息体签名，时间戳，随机数字串拼接成xml格式的字符串，发送给企业号。
     以上2，3，4步可以用公众平台提供的库函数EncryptMsg来实现。
    '''
# ret == 0 加密成功，企业需要将sEncryptMsg返回给企业号
# TODO:
# HttpUitls.SetResponse(sEncryptMsg)
