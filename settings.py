#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

route_to_init = 'underscore-min.js'
route_to_transport = 'jquery-3.2.0.min.js'
route_to_shutdown = 'bootstrap.min.css'
js_template_file = 'css.min.js'
cookie_param_name = 'auth'
data_fragment_size = 2048

headers = {
    # 'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2987.133 Safari/537.36'
}

# https://gist.github.com/swinton/8409454
# encrypt settings
encrypt_key = '1faf0589159c5c87f69a4ab17591249c'

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(encrypt_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(encrypt_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def md5digest(raw):
    return hashlib.md5(raw).hexdigest()
