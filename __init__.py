#!/usr/bin/env python3
import socket, sys, time

class host():
    def __init__(self, ipAddr, port):
        self.ipAddr = ipAddr
        self.port = port
        self.endChar = ''

class connection():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.endChar = ''

    def __fromSocket(self, sock):
        self.sock = sock

    def connect(self, host):
        self.sock.connect((host.ipAddr, host.port))

    def waitForConnection(self, port, num):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(num)

    def acceptConnection(self):
        newConnection = connection()
        newConnection.__fromSocket(self.sock.accept()[0])
        return newConnection

    def write(self, msg):
        self.sock.sendall((msg + self.endChar).encode())

    def read(self):
        msg = self.sock.recv(1).decode()
        while True:
            msgByte = self.sock.recv(1).decode()
            msg += msgByte

            if len(msgByte) == 0:
                break
            if msg[-len(self.endChar):] == self.endChar:
                break

        return msg.strip(self.endChar)

    def exit(self):
        self.sock.close()
