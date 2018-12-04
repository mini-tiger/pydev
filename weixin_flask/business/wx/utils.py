# coding=utf-8

from settings import baseconfig
from WXBizMsgCrypt import WXBizMsgCrypt


def wxGet(**kw):
    wxcpt = WXBizMsgCrypt(baseconfig.sToken, baseconfig.sEncodingAESKey, baseconfig.sCorpID)  ##k加载wxcpt

    sVerifyMsgSig = kw.get("msg_signature")
    sVerifyTimeStamp = kw.get("timestamp")
    sVerifyNonce = kw.get("nonce")
    sVerifyEchoStr = kw.get("echostr")

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