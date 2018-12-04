# coding:utf-8
from __future__ import absolute_import
from bk_site.weixin import wx_bp
from flask import jsonify
from flask import g, request

import logging

LOG = logging.getLogger(__name__)
############################################################
from business.wx.utils import WeixinInterface  # 已经加入sys.path 忽略报错



WX=WeixinInterface()
@wx_bp.route('/weixin', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # sVerifyMsgSig = request.args.get("msg_signature")
        # sVerifyTimeStamp = request.args.get("timestamp")
        # sVerifyNonce = request.args.get("nonce")
        # sVerifyEchoStr = request.args.get("echostr")
        # print sVerifyEchoStr,sVerifyMsgSig,sVerifyNonce,sVerifyTimeStamp
        # print wxGet(request.args)
        LOG.debug("WeiXin Check args %s" % request.args)
        return WX.WxGET(request.args)


    if request.method == "POST":
        LOG.debug("WeiXin Post args %s" % request.args)
        LOG.debug("WeiXin Post data %s" % request.data)
        return WX.WxPOST(request.args, request.data)
# return redirect(url_for('blue_recover.login', name="admin@localhost.org", _external=True))

@wx_bp.route('/sendmsg', methods=["GET", "POST"])
def send_msg():
    if request.method == "GET":
        # sVerifyMsgSig = request.args.get("msg_signature")
        # sVerifyTimeStamp = request.args.get("timestamp")
        # sVerifyNonce = request.args.get("nonce")
        # sVerifyEchoStr = request.args.get("echostr")
        # print sVerifyEchoStr,sVerifyMsgSig,sVerifyNonce,sVerifyTimeStamp
        # print wxGet(request.args)
        LOG.debug("WeiXin Check args %s" % request.args)
        return WX.WxGET(request.args)


    if request.method == "POST":
        LOG.debug("WeiXin Post args %s" % request.args)
        LOG.debug("WeiXin Post data %s" % request.data)
        return WX.WxPOST(request.args, request.data)