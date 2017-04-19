#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight
import base64

from Crypto.Cipher import AES

route_to_init = 'underscore-min.js'
route_to_transport = 'jquery-3.2.0.min.js'
route_to_shutdown = 'bootstrap.min.css'
cookie_param_name = 'auth'
data_fragment_size = 2048

headers = {
    # 'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2987.133 Safari/537.36'
}

# encrypt settings
encrypt_key = '1faf0589159c5c87'
encrypt_iv_ = 'f69a4ab17591249c'
encryptor = AES.new(encrypt_key, AES.MODE_CBC, encrypt_iv_)

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def encrypt(message):
    try:
        ciphertext = encryptor.encrypt(pad(message))
        return base64.b64encode(ciphertext)
    except:
        return ''


def decrypt(message):
    try:
        decodedstr = base64.b64decode(message)
        return unpad(encryptor.decrypt(decodedstr))
    except:
        return ''
