import hashlib
import secrets
import csv


class Generator_range_lamport:
    def __init__(self):
        self.secret_key = []
        self.public_key = []
        self.crypto_sign = []

    def write_message(self):
        message = str(input("Please, input a message: "))
        self.translate_the_message_to_hash(message)

    def translate_the_message_to_hash(self, message):
        hash_message = hashlib.md5(message.encode())
        print(hash_message.hexdigest())
        len_of_hash = len(hash_message.hexdigest())
        self.generate_secret_key(len_of_hash)

    def generate_secret_key(self, len_of_hash):
        for i in range(len_of_hash):
            self.secret_key.append([secrets.randbits(11), secrets.randbits(11)])
        self.generate_public_key()

    def generate_public_key(self):
        for i in self.secret_key:
            self.public_key.append([hashlib.new("sha3_224", (str(i[0])).encode()).hexdigest(),
                                    hashlib.new("sha3_224", (str(i[1])).encode()).hexdigest()])
        print(self.public_key)
        self.generate_crypto_sign()

    def generate_crypto_sign(self):
        print("Генерация секретного ключа")
        print(self.secret_key)
        for i in range(len(self.secret_key)):
            for j in range(1):
                if i % 2 != 0:
                    self.crypto_sign.append(self.secret_key[i][1])
                else:
                    self.crypto_sign.append(self.secret_key[i][0])
        print("Генерация подписи")
        print(self.crypto_sign)
        self.write_to_csv()

    def write_to_csv(self):
        with open("public_key.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.public_key)
        with open("crypto_sign.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(self.crypto_sign)


class Check_Crypto_Sign:
    def __init__(self):
        self.crypto_sign = []
        self.crypto_sign_hash = []
        self.public_key = []
    def reading_csv(self):
        # getting crypto_sign
        with open("crypto_sign.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(len(row)):
                    self.crypto_sign.append(row[i])

        #getting public key
        with open("public_key.csv","r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.public_key.append(row)
            self.translate_sign_to_hash()
    def translate_sign_to_hash(self):
        for i in self.crypto_sign:
            self.crypto_sign_hash.append(hashlib.new("sha3_224", i.encode()).hexdigest())
        self.check_sign()
    def check_sign(self):
        num = 0
        for i in range(len(self.public_key)):
            if self.crypto_sign_hash[i] in self.public_key[i]:
                num += 1
        if num == len(self.public_key):
            print("\nSuccess")
        else:
            print("\nError")

g = Generator_range_lamport()
g.write_message()

Check = Check_Crypto_Sign()
Check.reading_csv()
