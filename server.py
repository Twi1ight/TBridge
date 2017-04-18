#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight

import sys
import socket
import select

from bottle import request, run, route, error

from settings import route_to_transport, route_to_init, route_to_shutdown
from settings import encrypt, decrypt, post_param_name


@error(404)
@error(405)
def error404(err):
    return '404 Not Found.'


def invoke_service(data):
    sock.sendall(data)
    ret = ''
    while True:
        r, _, _ = select.select([sock], [], [], 0.1)
        if r:
            ret += sock.recv(4096)
            if len(ret) == 0:
                print 'service sock closed'
                break
        else:
            print 'service data length', len(ret)
            break
    return ret


@route('/%s' % route_to_transport, method='POST')
def transport():
    raw = request.forms[post_param_name]
    data = decrypt(raw)
    ret = invoke_service(data)
    return encrypt(ret)


@route('/%s' % route_to_init)
def init():
    global sock
    shutdown()
    try:
        sock = socket.socket()
        sock.connect((service_host, service_port))
    except Exception as e:
        return 'transport init failed: ', e
    return 'transport inited.'


@route('/%s' % route_to_shutdown)
def shutdown():
    try:
        sock.close()
    except:
        pass
    return 'transport stopped.'


def argparse():
    if len(sys.argv) != 4:
        print 'usage: python server.py port-for-client service-host service-port'
        print 'e.g. for ssh: python server.py 8089 localhost 22'
        sys.exit()
    return int(sys.argv[1]), sys.argv[2], int(sys.argv[3])


if __name__ == '__main__':
    webserv_port, service_host, service_port = argparse()
    # webserv_port, service_host, service_port = 8089, 'localhost', 22
    sock = None
    run(server='cherrypy', host='0.0.0.0', port=webserv_port, debug='debug')
