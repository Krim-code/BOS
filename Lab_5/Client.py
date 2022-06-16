import socket
import pickle

import random
from Cryptodome.Util.number import *


class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9098))
        self.n = 0
        self.s = 0
        self.v = 0

    def input(self):
        self.message = str(input("please input message: "))
        self.send(b"start")
        self.n = int(self.recv())

        self.confirm_data_to_decimal_form()

        self.v = pow(self.s, 2, self.n)
        print(f"N : {self.n}\n"
              f"S : {self.s}\n"
              f"V : {self.v}\n")

        self.send(str(self.v).encode("utf-8"))
        self.check_data()

    def check_data(self):
        no_of_iterations = 40
        for i in range(no_of_iterations):
            r = random.randint(1, self.n - 1)
            x = pow(r, 2, self.n)

            self.send(str(x).encode("utf-8"))

            e = int(self.recv())

            y = (r * (self.s ** e)) % self.n
            self.send(str(y).encode("utf-8"))

    def send(self, data):
        self.socket.send(data)

    def confirm_data_to_decimal_form(self):
        self.s = bytes_to_long(self.message.encode("utf-8"))

    def recv(self):
        tmp = self.socket.recv(1024)
        tmp = tmp.decode("utf8")
        return tmp


if __name__ == '__main__':
    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication.input()