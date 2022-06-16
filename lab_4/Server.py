import socket
import threading
import time
import secrets
import pyaes
import pickle
class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 5000))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            if self.transform_the_data(data) == True:
                results = "Success"
            else:
                results = "Error"
            self.conn.send(results.encode("utf-8"))

    def transform_the_data(self, dict):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        print(f"data: {data_pikles['data']}\n"
              f"time: {data_pikles['time']}\n"
              f"id: {data_pikles['id']}")
        return self.check_data(data_pikles['data'],data_pikles['time'],data_pikles['id'])
    def check_data(self,data,timer_check,id):
        timer = time.asctime()
        if timer_check == timer and id == self.id:
            return True
        else:
            return False

class One_Pass_Authentication_with_num:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 5001))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            try:
                data = data.decode("utf-8")
                self.num = secrets.randbelow(1000)
                self.conn.send(str(self.num).encode("utf-8"))
                self.recv()

            except UnicodeDecodeError:
                if self.transform_the_data(data) == True:
                    results = "Success"
                else:
                    results = "Error"
                self.conn.send(results.encode("utf-8"))

    def transform_the_data(self, dict):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        print(f"data: {data_pikles['data']}\n"
              f"num: {data_pikles['num']}\n"
              f"id: {data_pikles['id']}")
        return self.check_data(data_pikles['data'],data_pikles['num'],data_pikles['id'])
    def check_data(self,data,num_check,id):
        timer = time.asctime()
        if num_check == str(self.num) and id == self.id:
            return True
        else:
            return False

class Two_Pass_Authentication_with_num:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 5002))
        self.key = "This_key_for_demo_purposes_only!"
        self.id = "Bob"

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            try:
                data = data.decode("utf-8")
                self.num = secrets.randbelow(1000)
                self.conn.send(str(self.num).encode("utf-8"))
                self.recv()

            except UnicodeDecodeError:
                if self.transform_the_data(data) == True:
                    results = "Success"
                else:
                    results = "Error"
                dict = {"result": results,"numA": self.numA}
                results = pickle.dumps(dict)
                self.conn.send(results)

    def transform_the_data(self, dict):
        self.key = self.key.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.key)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        self.numA = data_pikles['numA']
        print(f"data: {data_pikles['data']}\n"
              f"num: {data_pikles['num']}\n"
              f"id: {data_pikles['id']}\n"
              f"num a: {data_pikles['numA']}")
        return self.check_data(data_pikles['data'],data_pikles['num'],data_pikles['id'])
    def check_data(self,data,num_check,id):
        if num_check == str(self.num) and id == self.id:
            return True
        else:
            return False

One_Pass_Authentication = One_Pass_Authentication()
One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()

One_Pass_Authentication = One_Pass_Authentication_with_num()
One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()

Two_Pass_Authentication = Two_Pass_Authentication_with_num()
One_Pass_Authentication_thread = threading.Thread(target=Two_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()