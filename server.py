#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight

import socket
import select
import base64

from bottle import request, run, route, error


# pip install "cherrypy>=3.0.8,<9.0.0"

@error(404)
def error404(error):
    return '404 Not Found.'


def communication(data):
    global sock
    sock.sendall(data)
    ret = ''
    while True:
        r, _, _ = select.select([sock], [], [], 0.1)
        if r:
            ret += sock.recv(1024)
            if len(ret) == 0:
                print 'sock closed'
                break
        else:
            print 'no more data', len(data)
            break
    return ret


@route('/server', method='POST')
def server():
    raw = request.forms['data']
    data = base64.b64decode(raw)
    ret = communication(data)
    return base64.b64encode(ret)


@route('/init')
def init():
    global sock
    shutdown()
    try:
        sock = socket.socket()
        sock.connect(('127.0.0.1', 22022))
    except Exception as e:
        return e
    return 'done'


@route('/shutdown')
def shutdown():
    global sock
    try:
        sock.close()
    except:
        pass
    return 'done'


if __name__ == '__main__':
    sock = None
    run(server='cherrypy', host='0.0.0.0', port=8089)
