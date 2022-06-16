import socket
import pickle

import random
from Cryptodome.Util.number import *


class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9098))
        self.a = 0
        self.p = 0
        self.g = 0
        self.A = 0
    def input(self):
        self.a = getPrime(125)
        self.p = getPrime(15)
        self.g = self.primitive_root(self.p)
        self.A = pow(self.g,self.a,self.p)
        print(f"{self.a=}\n"
              f"{self.p=}\n"
              f"{self.g=}\n"
              f"{self.A=}")
        message = self.create_public_message()
        self.send(message)
        self.B = int(self.recv())
        self.K = pow(self.B,self.a,self.p)
        print(f"K = {self.K}" )

    def create_public_message(self):
        dict = {"A": self.A, "P": self.p, "G": self.g}
        data_pickle = pickle.dumps(dict)
        return data_pickle

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        tmp = self.socket.recv(1024)
        tmp = tmp.decode("utf8")
        return tmp

    def gcd(self,a, b):
        while a != b:
            if a > b:
                a = a - b
            else:
                b = b - a
        return a

    def primitive_root(self,modulo):
        required_set = set(num for num in range(1, modulo) if self.gcd(num, modulo) == 1)
        for g in range(1, modulo):
            actual_set = set(pow(g, powers) % modulo for powers in range(1, modulo))
            if required_set == actual_set:
                break
        return g




if __name__ == '__main__':
    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication.input()