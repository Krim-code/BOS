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


class Registration:

    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9096))

    def connect(self):
        self.socket.listen(0)
        print("Registration listening:")
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
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        return login, password

    def check_data(self, login, password):
        db = sqlite3.connect("server.db")
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        password TEXT
        )""")
        db.commit()

        sql.execute(f"SELECT login FROM users WHERE login = '{login}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?,?)", (login, password))
            db.commit()
            return "Success"
        else:
            return "Error"


class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9098))

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
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


class Two_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9099))

    def connect(self):
        self.socket.listen(0)
        print("Two_Pass_Authentication listening:")
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


class One_Pass_Authentication_With_Confident:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9070))

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication_With_Confident listening:")
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
            check = self.check_for_confident(login, password)
            if check == "Success":
                results = self.check_data(login, password)
                self.conn.send(results.encode("utf-8"))
            else:
                self.conn.send(check.encode("utf-8"))

    def transform_the_data(self, dict):
        login = dict["login"]
        password = dict["password"]
        return login, password

    def check_for_confident(self, login, password):
        result = One_Pass_Send_to_Confidant().input(login, password)
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


class One_Pass_Send_to_Confidant:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9071))

    def input(self, login, password):
        self.login = login
        self.password = password
        return self.transform_the_data()

    def transform_the_data(self):
        dict = {"login": self.login, "password": self.password}
        data_pickle = pickle.dumps(dict)
        result = self.send_conf(data_pickle)
        return result

    def send_conf(self, data):
        self.socket.send(data)
        return self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        self.socket.close()
        return data.decode("utf-8")


class Two_Pass_Authentication_With_Confident:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9072))

    def connect(self):
        self.socket.listen(0)
        print("Two_Pass_Authentication_With_Confident listening:")
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
            # проверка третьего лица
            check_conf = self.check_for_confident(login, password)
            print(check_conf)
            if check_conf == "Success":
                if check_sign == "Success crypt":
                    results = self.check_data(login, password)
                    results = self.transform_the_data_for_crypto_answer(results)
                    self.conn.send(results)
                else:
                    results = self.transform_the_data_for_crypto_answer(check_sign)
                    self.conn.send(results)
            else:
                results = self.transform_the_data_for_crypto_answer(check_conf)
                self.conn.send(results)

    def check_for_confident(self, login, password):
        result = Two_Pass_Send_to_Confident().input(login, password)
        return result

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


class Two_Pass_Send_to_Confident:

    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9073))

    def input(self, login, password):
        self.login = login
        self.password = password
        return self.transform_the_data()

    def transform_the_data(self):
        self.generate_crypto_token()
        print(f"Генерация публичного ключа:\n{self.public_key}\n"
              f"Генерация криптоподписи: \n{self.crypto_sign}\n")
        dict = {"public_key": self.public_key, "crypto_sign": self.crypto_sign, "login": self.login,
                "password": self.password}
        data_pickle = pickle.dumps(dict)
        return self.send(data_pickle)

    def generate_crypto_token(self):
        self.public_key, self.crypto_sign = Generator_range_lamport().write_message(self.login)

    def send(self, data):
        self.socket.send(data)
        return self.recv()

    def recv(self):
        data = self.socket.recv(10024)
        dict = pickle.loads(data)
        crypto_sign = dict["crypto_sign"]
        public_key = dict["public_key"]
        result = self.check_sign(crypto_sign, public_key)
        self.socket.close()
        if result == "Success crypt":
            return (dict['result'])
        else:
            return ("ERROR")

    def check_sign(self, crypto_sign, public_key):
        result = Check_Crypto_Sign().reading_csv(crypto_sign, public_key)
        return result


Registration = Registration()
Registration_thread = threading.Thread(target=Registration.connect)
Registration_thread.start()

One_Pass_Authentication = One_Pass_Authentication()
One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
One_Pass_Authentication_thread.start()

Two_Pass_Authentication = Two_Pass_Authentication()
Two_Pass_Authentication_thread = threading.Thread(target=Two_Pass_Authentication.connect)
Two_Pass_Authentication_thread.start()

One_Pass_Authentication_With_Confident = One_Pass_Authentication_With_Confident()
One_Pass_Authentication_With_Confident_thread = threading.Thread(target=One_Pass_Authentication_With_Confident.connect)
One_Pass_Authentication_With_Confident_thread.start()

Two_Pass_Authentication_With_Confident = Two_Pass_Authentication_With_Confident()
Two_Pass_Authentication_With_Confident_thread = threading.Thread(target=Two_Pass_Authentication_With_Confident.connect)
Two_Pass_Authentication_With_Confident_thread.start()
