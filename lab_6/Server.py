import socket
import pickle
import threading
import random
from Cryptodome.Util.number import *

class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9098))
        self.n = 0
        self.v = 0

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf-8")
            if not data:
                break
            self.J = int(data)
            self.generate_n()
            print(f"N = {self.n}\n"
                  f"FI_N = {self.fi_n}\n"
                  f"E = {self.e}\n"
                  f"S = {self.s}\n"
                  f"X = {self.x}\n"
                  f"Y = {self.y}\n")
            public_key = self.create_public_message()
            self.conn.send(public_key)
            self.check_data()

    def create_public_message(self):
        dict = {"N": self.n, "E": self.e, "Y": self.y, "X": self.x}
        data_pickle = pickle.dumps(dict)
        return data_pickle

    def check_data(self):
        count = 0
        no_of_iterations = 40
        for i in range(no_of_iterations):
            a = self.recv_num()

            c = random.randint(0, self.e-1)
            self.conn.send(f"{c}".encode("utf-8"))

            z = self.recv_num()

            print("=====================================================")
            print("Iteration " + str(i + 1))
            print("a		= ", a)
            print("c 		= ", c)
            print("z 		= ", z)
            print("z**e 	= ", pow(z, self.e) % self.n)
            print("ay**c 	= ", (a * (self.y ** c)) % self.n)
            print("\nIteration " + str(i + 1) + ":	", end="")

            if (pow(z, self.e)% self.n == (a * (self.y ** c)) % self.n):
                print("Passed")
                count += 1
            else:
                print("Failed")

            print("=====================================================")

        if (count == no_of_iterations):
            print("Alice has the secret.")
        else:
            print("Alice does not have the secret.")
    def recv_num(self):
        data = self.conn.recv(1024)
        data = data.decode("utf-8")
        data = int(data)
        return data
    def generate_n(self):
        p = getPrime(10)
        q = getPrime(10)
        self.n = p * q
        self.fi_n = self.fi(self.n)
        self.e = random.randint(1,self.fi_n)
        self.s = pow(self.e,-1,self.n)
        self.x = pow(self.J,self.s*(-1),self.n)
        self.y = pow(self.x,self.e,self.n)

    def fi(self,n):
        f = n
        if n % 2 == 0:
            while n % 2 == 0:
                n = n // 2
            f = f // 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                while n % i == 0:
                    n = n // i
                f = f // i
                f = f * (i - 1)
            i = i + 2
        if n > 1:
            f = f // n
            f = f * (n - 1)
        return f


One_Pass_Authentication = One_Pass_Authentication()
One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()