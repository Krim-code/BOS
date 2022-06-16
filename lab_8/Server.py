import socket
import pickle
import threading
import random
from Cryptodome.Util.number import *
class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9098))
        self.b = 0
        self.B = 0
        self.A = 0
        self.g = 0
        self.p = 0
        self.K = 0
    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")

        self.b = getPrime(125)
        print(f"{self.b=}")
        public_key = self.recv_pickle()
        self.initialize(public_key)
        self.B = pow(self.g,self.b,self.p)
        self.K = pow(self.A,self.b,self.p)
        self.conn.send(f"{self.B}".encode("utf-8"))
        print(f"K = {self.K}")
    def recv_pickle(self):
        tmp = self.conn.recv(1024)
        try:
            tmp = pickle.loads(tmp)
            return tmp
        except:
            print("error")
    def initialize(self,public_key):
        self.A = public_key['A']
        self.g = public_key['G']
        self.p = public_key['P']
        print(public_key)


if __name__ == '__main__':
    # Generator_easy_pare = Generator_easy_pare()
    # Generator_easy_pare.initialize()

    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
    One_Pass_Authentication_thread.start()