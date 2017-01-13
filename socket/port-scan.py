# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:48:01 2016

@author: Henry
"""
import socket
import sys


def scanPort(host, port):
    sock = socket.socket()
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    if result == 0:
        print("port %d is open" % (port), flush=True)
    else:
        print("port %d is closed" % (port), flush=True)
    sock.close()


host = 'localhost'
if len(sys.argv) == 2 and sys.argv[1]:
    host = sys.argv[1]

print('Scanning %s' % (host,), flush=True)
for port in range(1, 1025):
    scanPort(host, port)
