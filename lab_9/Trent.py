import socket
import pickle
import threading
import random
import pyaes
from Cryptodome.Util.number import *

class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9098))
        self.A = ''
        self.B = ''
        self.Ra = ''
        self.K = "This_key_for_demo_purposes_onlT!"
        self.Ka = "This_key_for_demo_purposes_onlA!"
        self.Kb = "This_key_for_demo_purposes_onlB!"


    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        dict = self.recv()
        self.initialize_variable(dict)
        message = self.generate_answer()
        self.conn.send(message)

    def recv(self):
            data = self.conn.recv(1024)
            try:
                data = pickle.loads(data)
                return data
            except:
                print("error")

    def generate_answer(self):
        dict_b = {"K":self.K,"A":self.A}
        dict_b = pickle.dumps(dict_b)
        sign_dict_b = self.init_aes(dict_b,self.Kb)
        dict_a = {"Ra":self.Ra,"B":self.B,"K":self.K,"Kb_sign":sign_dict_b}
        dict_a = pickle.dumps(dict_a)
        sign_dict_a = self.init_aes(dict_a,self.Ka)
        return sign_dict_a
    def init_aes(self,dict,sign):
        key = sign.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(dict)
        return(ciphertext)
    def initialize_variable(self,data):
        self.A = data['A']
        self.B = data['B']
        self.Ra = data['Ra']
        print(data)
    def create_public_message(self):
        dict = {"N": self.n, "E": self.e, "Y": self.y, "X": self.x}
        data_pickle = pickle.dumps(dict)
        return data_pickle



if __name__ == '__main__':
    # Generator_easy_pare = Generator_easy_pare()
    # Generator_easy_pare.initialize()

    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
    One_Pass_Authentication_thread.start()