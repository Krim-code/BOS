import socket
import pickle
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
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9096))

    def input(self):
        self.login = str(input("Please input your login: "))
        self.password = str(input("Please input your password: "))
        self.transform_the_data()

    def transform_the_data(self):
        dict = {"login": self.login, "password": self.password}
        data_pickle = pickle.dumps(dict)
        self.send(data_pickle)

    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        print(data.decode("utf-8"))
        self.socket.close()


class One_Pass_Authentication:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9098))

    def input(self):
        self.login = str(input("Please input your login: "))
        self.password = str(input("Please input your password: "))
        self.transform_the_data()

    def transform_the_data(self):
        self.password = hashlib.md5(self.password.encode())
        self.password = self.password.hexdigest()
        dict = {"login": self.login, "password": self.password}
        data_pickle = pickle.dumps(dict)
        self.send(data_pickle)

    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        print(data.decode("utf-8"))
        self.socket.close()


class Two_Pass_Authentication:

    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9099))

    def input(self):
        self.login = str(input("Please input your login: "))
        self.password = str(input("Please input your password: "))
        self.transform_the_data()

    def transform_the_data(self):
        self.password = hashlib.md5(self.password.encode())
        self.password = self.password.hexdigest()
        self.generate_crypto_token()
        print(f"Генерация публичного ключа:\n{self.public_key}\n"
              f"Генерация криптоподписи: \n{self.crypto_sign}\n")
        dict = {"public_key": self.public_key, "crypto_sign": self.crypto_sign, "login": self.login,
                "password": self.password}
        data_pickle = pickle.dumps(dict)
        self.send(data_pickle)

    def generate_crypto_token(self):
        self.public_key, self.crypto_sign = Generator_range_lamport().write_message(self.login)

    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(10024)
        dict = pickle.loads(data)
        crypto_sign = dict["crypto_sign"]
        public_key = dict["public_key"]
        result = self.check_sign(crypto_sign, public_key)
        if result == "Success crypt":
            print(dict['result'])
        else:
            print("ERROR")
        self.socket.close()

    def check_sign(self, crypto_sign, public_key):
        result = Check_Crypto_Sign().reading_csv(crypto_sign, public_key)
        return result


class One_Pass_Authentication_With_Confidant:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9070))

    def input(self):
        self.login = str(input("Please input your login: "))
        self.password = str(input("Please input your password: "))
        self.transform_the_data()

    def transform_the_data(self):
        self.password = hashlib.md5(self.password.encode())
        self.password = self.password.hexdigest()
        dict = {"login": self.login, "password": self.password}
        data_pickle = pickle.dumps(dict)
        self.send(data_pickle)

    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(1024)
        print(data.decode("utf-8"))
        self.socket.close()


class Two_Pass_Authentication_With_Confidant:

    def __init__(self):
        self.login = ""
        self.password = ""
        self.socket = socket.socket()
        self.socket.connect(('localhost', 9072))

    def input(self):
        self.login = str(input("Please input your login: "))
        self.password = str(input("Please input your password: "))
        self.transform_the_data()

    def transform_the_data(self):
        self.password = hashlib.md5(self.password.encode())
        self.password = self.password.hexdigest()
        self.generate_crypto_token()
        print(f"Генерация публичного ключа:\n{self.public_key}\n"
              f"Генерация криптоподписи: \n{self.crypto_sign}\n")
        dict = {"public_key": self.public_key, "crypto_sign": self.crypto_sign, "login": self.login,
                "password": self.password}
        data_pickle = pickle.dumps(dict)
        self.send(data_pickle)

    def generate_crypto_token(self):
        self.public_key, self.crypto_sign = Generator_range_lamport().write_message(self.login)

    def send(self, data):
        self.socket.send(data)
        self.recv()

    def recv(self):
        data = self.socket.recv(10024)
        dict = pickle.loads(data)
        crypto_sign = dict["crypto_sign"]
        public_key = dict["public_key"]
        result = self.check_sign(crypto_sign, public_key)
        if result == "Success crypt":
            print(dict['result'])
        else:
            print("ERROR")
        self.socket.close()

    def check_sign(self, crypto_sign, public_key):
        result = Check_Crypto_Sign().reading_csv(crypto_sign, public_key)
        return result


if __name__ == '__main__':
    print("1. Registration\n"
          "2. One pass authentication\n"
          "3. Two pass authentication\n"
          "4. One pass authentication with_confidant\n"
          "5. Two pass authentication with_confidant")
    key = int(input("Please, input number of operation: "))
    if key == 1:
        Registration = Registration()
        Registration.input()
    if key == 2:
        One_Pass_Authentication = One_Pass_Authentication()
        One_Pass_Authentication.input()
    if key == 3:
        Two_Pass_Authentication = Two_Pass_Authentication()
        Two_Pass_Authentication.input()
    if key == 4:
        One_Pass_Authentication_with_confidant = One_Pass_Authentication_With_Confidant()
        One_Pass_Authentication_with_confidant.input()
    if key == 5:
        Two_Pass_Authentication_With_Confidant = Two_Pass_Authentication_With_Confidant()
        Two_Pass_Authentication_With_Confidant.input()
