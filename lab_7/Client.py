import socket
import pickle

import random
from Cryptodome.Util.number import *


class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9098))
        self.p = 48731
        self.q = 443
        self.g = 11444
        self.y = 7355
        self.w = 357

    def input(self):
        self.message = str(input("please input message: "))
        self.send("start".encode("utf-8"))
        self.check_data()
    def check_data(self):
        no_of_iterations = 6
        for i in range(no_of_iterations):
            r = random.randint(1, self.q - 1)
            x = pow(self.g, r, self.p)

            self.send(str(x).encode("utf-8"))

            e = int(self.recv())

            s = (r + (self.w * e)) % self.q
            self.send(str(s).encode("utf-8"))

    def send(self, data):
        self.socket.send(data)

    def confirm_data_to_decimal_form(self):
        self.s = bytes_to_long(self.message.encode("utf-8"))

    def recv(self):
        tmp = self.socket.recv(1024)
        tmp = tmp.decode("utf8")
        return tmp

    def recv_pickle(self):
        tmp = self.socket.recv(1024)
        try:
            tmp = pickle.loads(tmp)
            return tmp
        except:
            print("error")


if __name__ == '__main__':
    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication.input()