#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight

import base64
import socket

import requests

base_url = 'http://45.46.47.48:8089/%s'

proxy = {'http': 'http://22.161.218.94:3128'}


def send_data(buf):
    data = base64.b64encode(buf)
    print 'send data length', len(data)
    d = {'data': data}
    ret = url_request('POST', base_url % 'server', data=d)
    return base64.b64decode(ret)


def url_request(method, url, **kwargs):
    try:
        ret = requests.request(method, url, timeout=5, **kwargs).content
    except:
        ret = ''
    return ret


if __name__ == '__main__':
    socket = socket.socket()
    socket.bind(("127.0.0.1", 8080))
    socket.listen(1)
    conn, _ = socket.accept()
    print 'init', url_request('GET', base_url % 'init')
    while True:
        buf = conn.recv(1024)
        if len(buf) == 0:
            print 'client exited, shutdown server', url_request('GET', base_url % 'shutdown')
            break
        rdata = send_data(buf)
        conn.sendall(rdata)
