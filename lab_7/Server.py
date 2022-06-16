import socket
import pickle
import threading
import random
from Cryptodome.Util.number import *
class Generator_easy_pare():

    def __init__(self):
        self.p = 0
        self.q = 0
    def initialize(self):
        self.p = self.gen_p()
        self.q = self.gen_q(self.p-1)
        print(f"P: {self.p}\n"
              f"Q: {self.q}")
        g = self.find_g()
        print(g)
    def gen_p(self):
        return getPrime(40)
    def gen_q(self,num):
        Ans = self.Factor(num)
        return Ans[-2]
    def Factor(self,num):
        Ans = []
        d = 2
        while d * d <= num:
            if num % d == 0:
                Ans.append(d)
                num //= d
            else:
                if d % 2 !=0:
                    d += 2
                else:
                    d += 1
        if num > 1:
            Ans.append(num)
        return Ans



    def find_g(self):
        g = 2
        while (g**self.q) % self.p != 1:
            g += 1
        return g


class One_Pass_Authentication:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9098))
        self.p = 48731
        self.q = 443
        self.g = 11444
        self.y = 7355

    def connect(self):
        self.socket.listen(0)
        print("One_Pass_Authentication listening:")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected, {self.addr}")
        self.recv()

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf-8")
            if not data:
                break
            if data == "start":
                print("урааа")
                self.check_data()

    def create_public_message(self):
        dict = {"N": self.n, "E": self.e, "Y": self.y, "X": self.x}
        data_pickle = pickle.dumps(dict)
        return data_pickle

    def check_data(self):
        count = 0
        no_of_iterations = 6
        for i in range(no_of_iterations):
            x = self.recv_num()

            e = random.randint(0, 2**(no_of_iterations-1))
            self.conn.send(f"{e}".encode("utf-8"))

            s = self.recv_num()

            print("=====================================================")
            print("Iteration " + str(i + 1))
            print("x		= ", x)
            print("e		= ", e)
            print("s 		= ", s)
            print("g^s+y^e	= ", (pow(self.g, s) * pow(self.y,e)) %self.p)
            print("\nIteration " + str(i + 1) + ":	", end="")

            if ((pow(self.g, s)* pow(self.y,e))%self.p == x):
                print("Passed")
                count += 1
            else:
                print("Failed")

            print("=====================================================")

        if (count == no_of_iterations):
            print("Alice has the secret.")
        else:
            print("Alice does not have the secret.")
    def recv_num(self):
        data = self.conn.recv(1024)
        data = data.decode("utf-8")
        data = int(data)
        return data
    def generate_n(self):
        p = getPrime(10)
        q = getPrime(10)
        self.n = p * q
        self.fi_n = self.fi(self.n)
        self.e = random.randint(1,self.fi_n)
        self.s = pow(self.e,-1,self.n)
        self.x = pow(self.J,self.s*(-1),self.n)
        self.y = pow(self.x,self.e,self.n)

    def fi(self,n):
        f = n
        if n % 2 == 0:
            while n % 2 == 0:
                n = n // 2
            f = f // 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                while n % i == 0:
                    n = n // i
                f = f // i
                f = f * (i - 1)
            i = i + 2
        if n > 1:
            f = f // n
            f = f * (n - 1)
        return f



if __name__ == '__main__':
    # Generator_easy_pare = Generator_easy_pare()
    # Generator_easy_pare.initialize()

    One_Pass_Authentication = One_Pass_Authentication()
    One_Pass_Authentication_thread = threading.Thread(target=One_Pass_Authentication.connect)
    One_Pass_Authentication_thread.start()