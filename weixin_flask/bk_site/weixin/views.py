# coding:utf-8
from __future__ import absolute_import
from bk_site.weixin import wx_bp
from flask import jsonify
from flask import g, request

import logging

LOG = logging.getLogger(__name__)
############################################################
from business.wx.utils import wxGet


@wx_bp.route('/weixin', methods=["GET", "POST"])
def index():
	sVerifyMsgSig = request.form.get("msg_signature")
	sVerifyTimeStamp = request.form.get("timestamp")
	sVerifyNonce = request.form.get("nonce")
	sVerifyEchoStr = request.form.get("echostr")

	return wxGet(sVerifyEchoStr=sVerifyEchoStr,
	             sVerifyMsgSig=sVerifyMsgSig,
	             sVerifyNonce=sVerifyNonce,
	             sVerifyTimeStamp=sVerifyTimeStamp
	             )

# return redirect(url_for('blue_recover.login', name="admin@localhost.org", _external=True))
