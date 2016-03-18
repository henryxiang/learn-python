#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:10:53 2016

@author: Henry
"""
import socket
import time
import sys
import select

host = socket.gethostname()
port = 8888
EOL = b'\r\n'
userSockets = {}


def runServer():
    sock = socket.socket()

    try:
        sock.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error: %s' % (str(msg),))
        sys.exit()

    print('Server started on %s:%d' % (host, port))

    sock.listen(10)

    userSockets[sock] = ''

    while True:
        readyToRead, readToWrite, errors = select.select(
            userSockets.keys(), [], [])

        for s in readyToRead:
            if s == sock:
                clientsocket, addr = sock.accept()
                handleLogin(clientsocket)
            else:
                try:
                    # print('> client: ', s.getpeername())
                    handleIncomingData(s)
                except:
                    continue


def sendPrompt(sock):
    username = userSockets[sock]
    prompt = username + ': '
    try:
        sock.sendall(prompt.encode('ascii'))
    except:
        return


def handleLogin(sock):
    addr = sock.getpeername()
    print("Client connected from from %s:%d" % addr)

    username = login(sock)

    if username:
        userSockets[sock] = username
        sendGreetings(sock)
        msg = '[%s entered room]' % (username,)
        broadcast(sock, msg)
    else:
        print("Login failed")
        sock.close()


def sendGreetings(sock):
    addr = sock.getpeername()
    username = userSockets[sock]
    msg = "%s logged in from %s:%d " % (username, *addr)
    msg += "at " + time.ctime(time.time()) + '\r\n'
    sock.send(msg.encode('ascii'))
    # sendPrompt(sock)


def login(sock, retry=3):
    try:
        sock.sendall(b'Username: ')
        username = sock.recv(1024).rstrip(EOL).decode('ascii')
        if username in userSockets.values():
            msg = 'User %s has already logged in' % (username,)
            print(msg)
            sock.send(msg.encode('ascii') + EOL)
            sock.close()
            return ''
        for _ in range(retry):
            sock.sendall(b'Password: ')
            password = sock.recv(1024).rstrip(EOL).decode('ascii')
            # print("username=%s, password=%s" % (username, password))
            if password == 'password':
                print('password correct')
                return username
            else:
                sock.sendall(b'Incorrect password\r\n')
    except:
        print("Login error")

    return ''


def handleIncomingData(sock):
    addr = sock.getpeername()
    username = userSockets[sock]
    data = sock.recv(1024).rstrip(EOL).decode('ascii')
    if data == '.exit':
        sock.send(b'Bye!' + EOL)
        sock.close()
        del(userSockets[sock])
        msg = '[%s left room]' % (username,)
        broadcast(sock, msg)
        print("Client disconnected from from %s:%d" % addr)
    else:
        response = '%s: %s' % (username, data)
        broadcast(sock, response)


def broadcast(fromSock, msg):
    outMessage = msg + '\r\n'
    for sock in userSockets.keys():
        if (sock != fromSock and userSockets[sock]):
            try:
                sock.sendall(outMessage.encode('ascii'))
                # sendPrompt(sock)
            except:
                continue


if __name__ == '__main__':
    runServer()
