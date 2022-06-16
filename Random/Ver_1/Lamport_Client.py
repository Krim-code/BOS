import hashlib
import random
import socket
from threading import Thread

class Write_Message():
    def __init__(self):
        self.input_string = ""

    def write_message(self):
        self.input_string = str(input("Введите сообщение: "))
        return self.hash_message(self.input_string)

    def hash_message(self, message):
        hash = hashlib.sha3_224(message.encode())
        range_of_hash = len(hash.hexdigest())
        print(f"hash сообщения: {hash.hexdigest()}")
        print(f"длина hash'a: {range_of_hash}")
        return range_of_hash

class Pair_Range_Generator:
    def __init__(self,range_of_hash):
        self.range_of_hash = range_of_hash
        self.array_pair = []
        self.array_hash_pair =[]
    def generate_pair(self):
        for i in range(self.range_of_hash):
            self.array_pair.append((str(random.randint(1000, 9999)),str(random.randint(1000, 9999))))
        print(f"Сгенерированные пары случайных чисел или секретный ключ:\n{self.array_pair}")
        return self.generate_hash_pair()
    def generate_hash_pair(self):
        for i in self.array_pair:
            self.array_hash_pair.append((hashlib.new("sha3_224", i[0].encode()).hexdigest(),
                                         hashlib.new("sha3_224", i[1].encode()).hexdigest()))
        print(f"Захешированные пары или публичный ключ:\n{self.array_hash_pair}")
        return self.return_data()
    def return_data(self):
        return self.array_hash_pair, self.array_pair

class Send_Message():
    def __init__(self,public_key):
        self.public_key = public_key
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.connect(("127.0.0.1", 9096))  # localhost, port


    def send_server(self,something):  # старт клиента

            self.client.send(something)  # send message on the server
    def send_publick_key(self):
        self.send_server(public_key)


temp = Write_Message()
hash = temp.write_message()
print(hash)
check = Pair_Range_Generator(hash)
secret_key, public_key = check.generate_pair()
send = Send_Message(public_key)
send.send_publick_key()


