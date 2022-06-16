import pickle
import secrets
import socket
import time

import pyaes



class One_Pass_Authentication_with_time:
    def __init__(self):
        self.data = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 5000))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"


    def input(self):
        self.data = str(input("Please input your message: "))
        self.transform_the_data()

    def transform_the_data(self):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        timer = time.asctime()
        dict = {"data": self.data, "time": timer, "id":self.id}
        data_pickle = pickle.dumps(dict)
        ciphertext = aes.encrypt(data_pickle)
        self.send(ciphertext)


    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        print(data.decode("utf-8"))
        self.socket.close()

class One_Pass_Authentication_with_num:
    def __init__(self):
        self.data = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 5001))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"


    def input(self):
        self.data = str(input("Please input your message: "))
        self.send("Start".encode("utf-8"))
        self.recv()

    def transform_the_data(self):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        timer = time.asctime()
        dict = {"data": self.data, "num": self.num, "id":self.id}
        data_pickle = pickle.dumps(dict)
        ciphertext = aes.encrypt(data_pickle)
        self.send(ciphertext)


    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        self.num = str(data.decode("utf-8"))
        print(self.num)
        if self.num == "Success":
            print("Fully Success")
        else:
            self.transform_the_data()

class Two_Pass_Authentication_with_num:
    def __init__(self):
        self.data = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 5002))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"


    def input(self):
        self.data = str(input("Please input your message: "))
        self.send("Start".encode("utf-8"))
        self.recv()

    def transform_the_data(self):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        self.numA = secrets.randbelow(1000)
        dict = {"data": self.data, "num": self.num,"numA":self.numA, "id":self.id}
        data_pickle = pickle.dumps(dict)
        ciphertext = aes.encrypt(data_pickle)
        self.send(ciphertext)


    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        try:
            data = data.decode("utf-8")
            self.num = str(data)
            print(self.num)
            if self.num == "Success":
                print("Fully Success")
            else:
                self.transform_the_data()
        except UnicodeDecodeError:
            print("Resulp")
            data = pickle.loads(data)
            if data["numA"] == self.numA:
                print("Successful")
            else:
                print("Errors")


if __name__ == '__main__':
    key = int(input("Please select Authentication version: \n"
                    "1. One_Pass_Authentication_with_time\n"
                    "2. One_Pass_Authentication_with_num\n"
                    "3. Two_Pass_Authentication_with_num"))
    if key == 1:
        One_Pass_Authentication = One_Pass_Authentication_with_time()
        One_Pass_Authentication.input()
    if key == 2:
        One_Pass_Authentication = One_Pass_Authentication_with_num()
        One_Pass_Authentication.input()
    if key == 3:
        Two_Pass_Authentication_with_num = Two_Pass_Authentication_with_num()
        Two_Pass_Authentication_with_num.input()