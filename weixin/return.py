#-*- coding:utf-8 -*-
from flask import Flask,request
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
app = Flask(__name__)
@app.route('/index',methods=['GET','POST'])
def index():
    sToken = 'weixin'
    sEncodingAESKey = 'BQptm8SueWbIj8z1NRPNSxdznzSAmRMiP54cKSmCsQh'
    sCorpID = 'wx0a5e0ea42d34d2e1'
    wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
    #获取url验证时微信发送的相关参数
    sVerifyMsgSig=request.args.get('msg_signature')
    sVerifyTimeStamp=request.args.get('timestamp')
    sVerifyNonce=request.args.get('nonce')
    sVerifyEchoStr=request.args.get('echostr')
    #
    sReqMsgSig = sVerifyMsgSig
    sReqTimeStamp = sVerifyTimeStamp
    sReqNonce = sVerifyNonce
    #
    sResqMsgSig = sVerifyMsgSig
    sResqTimeStamp = sVerifyTimeStamp
    sResqNonce = sVerifyNonce
    #验证url
    if request.method == 'GET':
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        print type(ret)
        print type(sEchoStr)
        if (ret != 0 ):
            print "ERR: VerifyURL ret:" + ret
            sys.exit(1)
        return sEchoStr
    #接收客户端消息
    if request.method == 'POST':
        #sReqMsgSig = request.form.get('msg_signature')
        #sReqTimeStamp = request.form.get('timestamp')
        #sReqNonce = request.form.get('nonce')
        #赋值url验证请求相同的参数，使用上面注释掉的request.form.get方式获取时，测试有问题
        sReqMsgSig = sVerifyMsgSig
        sReqTimeStamp = sVerifyTimeStamp
        sReqNonce = sVerifyNonce
        sReqData = request.data
        print sReqData
        ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if (ret != 0):
            print "ERR: VerifyURL ret:"
            sys.exit(1)
        #解析发送的内容并打印
        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text
        print content
    #被动响应消息，将微信端发送的消息返回给微信端
    sRespData = '''<xml>
            <ToUserName><![CDATA[mycreate]]></ToUserName>
            <FromUserName><![CDATA[wx177d1233ab4b730b]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[''' +content +''']]></Content>
            <MsgId>1234567890123456</MsgId>
            <AgentID>1</AgentID>
            </xml>'''
    ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
    if( ret!=0 ):
        print "ERR: EncryptMsg ret: " + ret
        sys.exit(1)
    return sEncryptMsg

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8008,debug=True)