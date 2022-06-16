import socket
import pickle
import threading
import sqlite3
import hashlib
import secrets


class Check_Crypto_Sign:
    def __init__(self):
        self.crypto_sign = []
        self.crypto_sign_hash = []
        self.public_key = []

    def reading_csv(self, crypto_sign, public_key):
        # getting crypto_sign
        self.public_key = public_key
        self.crypto_sign = crypto_sign
        result = self.translate_sign_to_hash()
        return result

    def translate_sign_to_hash(self):
        for i in self.crypto_sign:
            self.crypto_sign_hash.append(hashlib.new("sha3_224", str(i).encode()).hexdigest())
        result = self.check_sign()
        return result

    def check_sign(self):
        num = 0
        for i in range(len(self.public_key)):
            if self.crypto_sign_hash[i] in self.public_key[i]:
                num += 1
        if num == len(self.public_key):
            result = "Success crypt"
        else:
            result = "Error"
        return result


class Generator_range_lamport(object):
    def __init__(self):
        self.secret_key = []
        self.public_key = []
        self.crypto_sign = []

    def write_message(self, message):
        public_key, crypto_sign = self.translate_the_message_to_hash(message)
        return public_key, crypto_sign

    def translate_the_message_to_hash(self, message):
        hash_message = hashlib.md5(message.encode())
        len_of_hash = len(hash_message.hexdigest())
        public_key, crypto_sign = self.generate_secret_key(len_of_hash)
        return public_key, crypto_sign

    def generate_secret_key(self, len_of_hash):
        for i in range(len_of_hash):
            self.secret_key.append([secrets.randbits(11), secrets.randbits(11)])
        public_key, crypto_sign = self.generate_public_key()
        return public_key, crypto_sign

    def generate_public_key(self):
        for i in self.secret_key:
            self.public_key.append([hashlib.new("sha3_224", (str(i[0])).encode()).hexdigest(),
                                    hashlib.new("sha3_224", (str(i[1])).encode()).hexdigest()])
        print(self.public_key)
        public_key, crypto_sign = self.generate_crypto_sign()
        return public_key, crypto_sign

    def generate_crypto_sign(self):
        for i in range(len(self.secret_key)):
            for j in range(1):
                if i % 2 != 0:
                    self.crypto_sign.append(self.secret_key[i][1])
                else:
                    self.crypto_sign.append(self.secret_key[i][0])
        return self.public_key, self.crypto_sign


class Confident_Check:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9071))

    def connect(self):
        self.socket.listen(0)
        print("Confident_Check listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            try:
                dict = pickle.loads(data)
            except EOFError:
                break
            login, password = self.transform_the_data(dict)
            results = self.check_data(login, password)
            self.conn.send(results.encode("utf-8"))

    def transform_the_data(self, dict):
        login = dict["login"]
        password = dict["password"]
        return login, password

    def check_data(self, login, password):
        db = sqlite3.connect("server.db")
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        password TEXT
        )""")
        db.commit()

        sql.execute(f"SELECT login FROM users WHERE login = '{login}' AND password = '{password}'")
        if sql.fetchone() is None:
            db.commit()
            return "Error"
        else:
            return "Success"


class Confident_Check_Two_Pass:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9073))

    def connect(self):
        self.socket.listen(0)
        print("Confident_Check_Two_Pass listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(10096)
            try:
                dict = pickle.loads(data)
            except EOFError:
                break
            crypto_sign, public_key, login, password = self.transform_the_data(dict)
            check_sign = self.check_sign(crypto_sign, public_key)
            if check_sign == "Success crypt":
                results = self.check_data(login, password)
                results = self.transform_the_data_for_crypto_answer(results)
                self.conn.send(results)
            else:
                self.conn.send(check_sign.encode("utf-8"))

    def transform_the_data_for_crypto_answer(self, result):
        self.generate_crypto_token(result)
        print(f"Генерация публичного ключа:\n{self.public_key}\n"
              f"Генерация криптоподписи: \n{self.crypto_sign}\n")
        dict = {"public_key": self.public_key, "crypto_sign": self.crypto_sign, "result": result}
        data_pickle = pickle.dumps(dict)
        return data_pickle

    def generate_crypto_token(self, result):
        self.public_key, self.crypto_sign = Generator_range_lamport().write_message(result)

    def transform_the_data(self, dict):
        crypto_sign = dict["crypto_sign"]
        public_key = dict["public_key"]
        login = dict["login"]
        password = dict["password"]
        return crypto_sign, public_key, login, password

    def check_sign(self, crypto_sign, public_key):
        result = Check_Crypto_Sign().reading_csv(crypto_sign, public_key)
        return result

    def check_data(self, login, password):
        db = sqlite3.connect("server.db")
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        password TEXT
        )""")
        db.commit()

        sql.execute(f"SELECT login FROM users WHERE login = '{login}' AND password = '{password}'")
        if sql.fetchone() is None:
            db.commit()
            return "Error"
        else:
            return "Success"


if __name__ == '__main__':
    Confident_Check = Confident_Check()
    Confident_Check = threading.Thread(target=Confident_Check.connect)
    Confident_Check.start()

    Confident_Check_Two_Pass = Confident_Check_Two_Pass()
    Confident_Check_Two_Pass = threading.Thread(target=Confident_Check_Two_Pass.connect)
    Confident_Check_Two_Pass.start()
