import socket
import pickle
import pyaes
import random
from Cryptodome.Util.number import *


class Send_to_Trent:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9098))
        self.A = "Alice"
        self.B = "Bob"
        self.Ra = 0
        self.Ka = "This_key_for_demo_purposes_onlA!"
        self.K = ''
        self.Kb_sign = ''

    def input(self):
        self.message = str(input("please input message: "))
        self.generate_Ra()
        message = self.create_pikle_message()
        self.send(message)
        answer_trent = self.recv()
        answer_trent = self.ancrypt_message(answer_trent)
        self.initialize_variable_for_B(answer_trent)
        return self.Ra, self.K ,self.Kb_sign
    def initialize_variable_for_B(self,dict):
        self.K = dict["K"]
        self.Kb_sign = dict["Kb_sign"]
    def create_return(self):
        pass
    def ancrypt_message(self,dict):
        self.Ka = self.Ka.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.Ka)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        return data_pikles
    def send(self, data):
        self.socket.send(data)
    def generate_Ra(self):
        self.Ra = random.randint(pow(10,5),pow(10,7))
    def create_pikle_message(self):
        dict = {"A": self.A, "B": self.B, "Ra": self.Ra}
        data_pickle = pickle.dumps(dict)
        return data_pickle
    def recv(self):
        tmp = self.socket.recv(1024)
        return tmp

    def recv_pickle(self):
        tmp = self.socket.recv(1024)
        try:
            tmp = pickle.loads(tmp)
            return tmp
        except:
            print("error")

class Send_to_server:
    def __init__(self,Ra,K,Kb_sign):
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9099))
        self.A = "Alice"
        self.B = "Bob"
        self.Ra = Ra
        self.Ka = "This_key_for_demo_purposes_onlA!"
        self.K = K
        self.Kb_sign = Kb_sign
        self.Rb = 0
        self.Rb1 = 0

    def input(self):
        self.send(self.Kb_sign)
        data = self.recv()
        data = self.ancrypt_message(data)
        self.Rb = data['Rb']
        self.Rb1 = self.Rb - 1
        dict = {"Rb1": self.Rb1}
        dict = pickle.dumps(dict)
        answer = self.init_aes(dict,self.K)
        self.send(answer)
        result = self.recv().decode('utf-8')
        print(f"Rb = {self.Rb}\n"
              f"Rb - 1 = {self.Rb1}\n"
              f"K = {self.K}\n"
              f"A = {self.A}\n"
              f"B = {self.B}\n"
              f"Ra = {self.Ra}\n"
              f"result = {result}")
    def init_aes(self,dict,key):
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(dict)
        return(ciphertext)

    def send(self, data):
        self.socket.send(data)
    def recv(self):
        tmp = self.socket.recv(1024)
        return tmp
    def ancrypt_message(self,dict):
        self.K = self.K.encode("utf-8")
        aes = pyaes.AESModeOfOperationCTR(self.K)
        decrypted = aes.decrypt(dict)
        data_pikles = pickle.loads(decrypted)
        return data_pikles

if __name__ == '__main__':
    Send_to_Trent = Send_to_Trent()
    Ra, K ,Kb_sign = Send_to_Trent.input()
    Send_to_server = Send_to_server(Ra, K ,Kb_sign)
    Send_to_server.input()
