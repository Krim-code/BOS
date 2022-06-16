import socket
import pickle
import threading
import random
import pyaes
from Cryptodome.Util.number import *

class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9099))
        self.Kb = "This_key_for_demo_purposes_onlB!"
        self.K = ""
        self.A = ""
        self.Rb = 0
        self.B = "Bob"


    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        data = self.recv()
        data = self.ancrypt_message(data,self.Kb)
        self.initialize_variable(data)
        self.generate_Rb()
        answer = self.create_message()
        answer = self.init_aes(answer,self.K)
        self.conn.send(answer)
        data = self.recv()
        data = self.ancrypt_message(data,self.K)
        data = data['Rb1']
        if data == self.Rb-1:
            result = "Success"
        else:
            result = "Error"
        self.conn.send(result.encode('utf-8'))
        print(f"Rb = {self.Rb}\n"
              f"Rb - 1 = {data}\n"
              f"K = {self.K}\n"
              f"A = {self.A}\n"
              f"B = {self.B}\n"
              f"result = {result}")
    def recv(self):
            data = self.conn.recv(1024)
            return data
    def generate_Rb(self):
        self.Rb = random.randint(pow(10,5),pow(10,7))
    def ancrypt_message(self,dict,sign):
        sign = sign.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(sign)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        return data_pikles
    def initialize_variable(self,dict):
        self.K = dict['K']
        self.A = dict['A']
    def init_aes(self,dict,sign):
        key = sign.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(dict)
        return(ciphertext)

    def create_message(self):
        dict = {"Rb": self.Rb}
        data_pickle = pickle.dumps(dict)
        return data_pickle



if __name__ == '__main__':
    # Generator_easy_pare = Generator_easy_pare()
    # Generator_easy_pare.initialize()

    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
    One_Pass_Authentication_thread.start()