# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:10:53 2016

@author: Henry
"""
import socket
import time
import sys

# sock = socket.socket()
# host = '127.0.0.1'
host = socket.gethostname()
port = 8888
# sock = socket.socket()
EOL = b'\r\n'


def read_data(sock, end=b'\r\n'):
    data = b''
    while True:
        buffer = sock.recv(1024)
        print(buffer, flush=True)
        if not buffer:
            sock.close()
            break
        if buffer[-2:] == end:
            data += buffer[:-2]
            break
        data += buffer
    return data


def runServer():
    sock = socket.socket()

    try:
        sock.bind((host, port))
    #    print('server started on %s:%d' % (host, port))
    except socket.error as msg:
        print('Bind failed. Error: %s' % (str(msg),), flush=True)
        sys.exit()

    # print('server started on %s:%d' % (host, port))
    print('Server started on %s:%d' % (host, port), flush=True)

    sock.listen(10)

    while True:
        clientsocket, addr = sock.accept()

        print("Client connected from from %s:%d" % addr, flush=True)

        username = login(clientsocket)

        if username:
            msg = "%s logged in from %s:%d " % (username, *addr)
            msg += "at " + time.ctime(time.time()) + '\r\n'
            clientsocket.send(msg.encode('ascii'))
            handleEcho(clientsocket, addr)
        else:
            print("Login failed")
            clientsocket.close()


def login(sock, retry=3):
    sock.sendall(b'Username: ')
    username = sock.recv(1024).rstrip(EOL).decode('ascii')

    for _ in range(retry):
        sock.sendall(b'Password: ')
        password = sock.recv(1024).rstrip(EOL).decode('ascii')
        # print("username=%s, password=%s" % (username, password))
        if password == 'password':
            print('password correct')
            return username
        else:
            sock.sendall(b'Incorrect password\r\n')

    return ''


def handleEcho(sock, addr):
    data = b''
    while True:
        # data = read_data(clientsocket)
        data = sock.recv(1024).rstrip(EOL)
        if data == b'.exit':
            sock.send(b'Bye!' + EOL)
            sock.close()
            print("Client disconnected from from %s:%d" % addr, flush=True)
            break
        else:
            sock.send(b'=> ' + data + EOL)
            data = b''
# print('Shutting down server', flush=True)
# sock.close()


if __name__ == '__main__':
    runServer()
