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
            if data.decode("utf-8") == "start":
                self.generate_n()
                print(self.n)
                self.conn.send(f"{self.n}".encode("utf-8"))
                self.v = int(self.conn.recv(1024).decode("utf-8"))
                print(f"N : {self.n}\n"
                      f"V : {self.v}\n")
                self.check_data()
            if not data:
                break

    def check_data(self):
        count = 0
        no_of_iterations = 40
        for i in range(no_of_iterations):
            x = self.recv_num()

            e = random.randint(0, 1)
            self.conn.send(f"{e}".encode("utf-8"))

            y = self.recv_num()

            print("=====================================================")
            print("Iteration " + str(i + 1))
            print("x		= ", x)
            print("e 		= ", e)
            print("y 		= ", y)
            print("y**2 		= ", pow(y, 2, self.n))
            print("(x*(v**e)) 	= ", (x * (self.v ** e)) % self.n)
            print("\nIteration " + str(i + 1) + ":	", end="")

            if (pow(y, 2, self.n) == (x * (self.v ** e)) % self.n):
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
        p = getPrime(15)
        q = getPrime(15)
        self.n = p * q


One_Pass_Authentication = One_Pass_Authentication()
One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()