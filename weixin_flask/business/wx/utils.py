# coding=utf-8

from settings import baseconfig
from WXBizMsgCrypt import WXBizMsgCrypt
import os, sys, time
import xml.etree.cElementTree as ET

import logging

LOG = logging.getLogger(__name__)

# def wxGet(kw):
#     wxcpt = WXBizMsgCrypt(baseconfig.sToken, baseconfig.sEncodingAESKey, baseconfig.sCorpID)  ##k加载wxcpt
#
#     sVerifyMsgSig = kw.get("msg_signature")
#     sVerifyTimeStamp = kw.get("timestamp")
#     sVerifyNonce = kw.get("nonce")
#     sVerifyEchoStr = kw.get("echostr")
#
#     '''
#        ret 代表wxcpt.VerifyURL 函数是否正确解析 正确是0，不正确非0,错误代码见ierror.py
#     '''
#
#     ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
#     if (ret != 0):
#         print "ERR: VerifyURL ret: " + str(ret)
#         return
#         '''
#         返回，否则程序会死掉
#         '''
#     # sys.exit(1)
#     else:
#         return sEchoStr  ##回调验证 返回明文

class WeixinInterface:
    def __init__(self):
        ##些函数作用请看WEB模块文章
        self.app_root = os.path.dirname(__file__)
        self.sToken = baseconfig.sToken
        self.sEncodingAESKey = baseconfig.sEncodingAESKey
        self.sCorpID = baseconfig.sCorpID

        # 获取输入参数

        self.wxcpt = WXBizMsgCrypt(self.sToken, self.sEncodingAESKey, self.sCorpID)  ##k加载wxcpt


    def WxGET(self, kw):
        # 获取输入参数
        sVerifyMsgSig = kw.get("msg_signature")
        sVerifyTimeStamp = kw.get("timestamp")
        sVerifyNonce = kw.get("nonce")
        sVerifyEchoStr = kw.get("echostr")

        '''
           ret 代表wxcpt.VerifyURL 函数是否正确解析 正确是0，不正确非0,错误代码见ierror.py
        '''
        ret, sEchoStr = self.wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
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
        LOG.debug("recv text is: %s" % content)
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
            LOG.error("recv text is: %s,ERR: EncryptMsg ret:" % content, str(ret))
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
        # eventkey = self.xml_tree.find("EventKey").text
        #
        self.event_key = self.xml_tree.find("EventKey").text
        LOG.debug("recv data XML eventKEY: %s" % self.event_key)
        createtime = str(int(time.time()))
        msg = "别瞎点：感谢陶钧对此次项目的极大支持"
        ##以下 为回复消息时的 ，加密过程
        sRespData = "<xml><ToUserName><![CDATA[{0}]]></ToUserName><FromUserName><![CDATA[{1}]]></FromUserName><CreateTime>{2}</CreateTime><MsgType><![CDATA[{3}]]></MsgType><Content><![CDATA[{4}]]></Content><AgentID>{5}</AgentID></xml>".format(
            self.fromuser, self.touser, createtime, msgtype, msg, self.AgentID)
        ret, sEncryptMsg = self.wxcpt.EncryptMsg(sRespData, self.sReqNonce, self.sReqTimeStamp)
        # print sRespData
        if (ret != 0):
            print "ERR: EncryptMsg ret: " + str(ret)
            sys.exit(1)
        return sEncryptMsg

    def WxPOST(self, kw, sReqData):
        # sReqData = web.data()  ##获取 加密的XML
        # data = web.input()  ##获取 参数
        # print sToken, sEncodingAESKey, sCorpID

        self.sReqMsgSig = kw.get("msg_signature")
        self.sReqTimeStamp = kw.get("timestamp")
        self.sReqNonce = kw.get("nonce")
        # sVerifyEchoStr = kw.get("echostr")


        ret, sMsg = self.wxcpt.DecryptMsg(sReqData, self.sReqMsgSig, self.sReqTimeStamp, self.sReqNonce)
        if (ret != 0):
            print "ERR: DecryptMsg ret: " + str(ret)
            return
        # sys.exit(1)
        # print sMsg
        self.xml_tree = ET.fromstring(sMsg)  ##sMsg  解密后的XML

        # print sMsg
        self.msgtype = self.xml_tree.find("MsgType").text
        self.touser = self.xml_tree.find("ToUserName").text
        self.fromuser = self.xml_tree.find("FromUserName").text
        self.AgentID = self.xml_tree.find("AgentID").text
        # self.event_key = self.xml_tree.find("EventKey").text
        # LOG.debug("recv data XML eventKEY: %s" % self.event_key)


        if self.msgtype == 'text':  ##通过类型判断 进入哪个函数
            return self.TEXT()
        elif self.msgtype == 'event':
            return self.EVENT()