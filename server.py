#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 2017/4/11
# @Author  : Twi1ight
import re
import sys
import socket
import select
import urllib

from bottle import request, run, route, error
from copy import copy

from settings import route_to_transport, route_to_init, route_to_shutdown, md5digest
from settings import encrypt, decrypt, cookie_param_name, js_template_file


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


@route('/%s' % route_to_transport)
def transport():
    raw = urllib.unquote(request.get_cookie(cookie_param_name))
    data = decrypt(raw)
    ret = invoke_service(data)
    ciphertext = encrypt(ret)
    # obfuscate data to js file
    body = copy(js_template)
    ciphers = splitn(ciphertext, len(placeholder))
    for i in range(len(placeholder)):
        body = body.replace(placeholder[i], '"%s"' % ciphers[i], 1)
    return body + '//%s' % md5digest(ciphertext)


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


def get_template(filename):
    with open(filename) as f:
        template = f.read()
    return template


def splitn(s, n):
    l = len(s) / n if len(s) % n == 0 else len(s) / n + 1
    array = [s[i:i + l] for i in xrange(0, len(s), l)]
    for _ in range(n - len(array)):
        array.append('')
    return array


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
    js_template = get_template(js_template_file)
    placeholder = re.findall('(".*?")', js_template)
    run(server='cherrypy', host='0.0.0.0', port=webserv_port, debug='debug')
