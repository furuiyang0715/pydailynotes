#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/3/15 下午4:43
# @Author : Katrinafu
# @Desc: 钉钉消息助手(python2)

import base64
import hashlib
import hmac
import json
import time
import traceback
import urllib
import requests


def ding(msg, secret, token, at=None, at_all=False):
    try:
        _ding(msg, secret, token, at, at_all)
    except:
        traceback.print_exc()


def _ding(msg, secret, token, at=None, at_all=False):
    """发送钉钉消息

        msg: 文本格式的消息
        secret:
        token:
        at: @指定的人员 需注册钉钉的手机号
        at_all: 是否 @所有人
    """

    def get_url(secret, token):
        timestamp = str(int(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.quote_plus(base64.b64encode(hmac_code))
        url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(
            token, timestamp, sign)
        return url

    url = get_url(secret, token)
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message = {
        "msgtype": "text",
        "text": {
            "content": "{}".format(msg)
        },
    }
    at_info = {"isAtAll": at_all}
    if at is not None:
        at_info.update({"atMobiles": [at, ], })
    message.update({"at": at_info})
    message_json = json.dumps(message)
    resp = requests.post(url=url, data=message_json, headers=header)
    if resp.status_code != 200:
        raise Exception("Status code not 200")
    else:
        resp_data = resp.json()
        if resp_data['errcode'] != 0:
            raise Exception(resp_data['errmsg'])
