import pyautogui as pag
import numpy as np
import time
import math
import sympy
import sys


class Generator_seed:
    def __init__(self):
        self.ten_numerical_range = ""
        self.array_ten_numerical_range = []
        self.array_position_cursor = []
        self.time_old = 0
        self.time_new = 0

    def insert_number(self,number):
        new_string = []
        string_number = str(number)
        sdvig = int(len(string_number)/10)
        for i in range(sdvig,len(string_number)-sdvig,2):
            new_string.append(string_number[i])
        new_string = int("".join(new_string))
        return new_string

    def check_position_cursor(self):
        while len(self.array_position_cursor) < 10:
            (position_cursor_old_x, position_cursor_old_y) = pag.position()
            time.sleep(0.2)
            (position_cursor_x, position_cursor_y) = pag.position()
            if (position_cursor_old_x, position_cursor_old_y) == (position_cursor_x, position_cursor_y):
                print("пожалуйста подвигайте мышью")
            else:
                self.array_position_cursor.append((position_cursor_x, position_cursor_y))
            print(self.array_position_cursor)
    def generate_ten_numerical_range(self,len_range):
        while len(str(self.ten_numerical_range)) < len_range:
            time.sleep(0.21)
            self.time_new = int((time.time() - math.floor(time.time())) * 10 ** 16)
            for i in self.array_position_cursor:
                key = str(((((i[0]*i[1])**2 % self.time_old**2)**6)%self.time_new**2)-23132)
                self.array_ten_numerical_range.append(self.insert_number(int(np.roll(key,int(key[4])))))
                print(self.array_ten_numerical_range)
            self.ten_numerical_range = self.insert_number(int("".join(map(str,self.array_ten_numerical_range))))
            print(self.ten_numerical_range)
        if len_range < len(str(self.ten_numerical_range)):
            care = len(str(self.ten_numerical_range)) - len_range
            self.ten_numerical_range = int(self.ten_numerical_range / 10**care)
            print(self.ten_numerical_range)
        return str(self.ten_numerical_range)
    def generate_bin_range(self,n):
        array_bin = []
        for i in n:
            if int(i)%2 == 0:
                array_bin.append(0)
            else:
                array_bin.append(1)
        return "".join(map(str,array_bin))










    def start_random(self,len_range):

        self.time_old = int((time.time() - math.floor(time.time())) * 10 ** 16)
        print(self.time_old)
        self.check_position_cursor()
        range_num_ten = self.generate_ten_numerical_range(len_range)
        range_num_bin = self.generate_bin_range(range_num_ten)
        print(range_num_bin)
        return range_num_ten


Rand = Generator_seed()

seed = int(Rand.start_random(100))

x = 3*10**10
y = 4*10**10

def write_txt(range_num):
    with open("hello.txt", "w") as file:
        file.write(range_num)

def lcm(a, b):
    return a * b / gcd(a, b)

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def next_usable_prime(x):
        p = sympy.nextprime(x)
        while (p % 4 != 3):
            p = sympy.nextprime(p)
        return p

p = next_usable_prime(x)
q = next_usable_prime(y)
M = p*q

N = 1000


if (len(sys.argv)>1):
    N=int(sys.argv[1])


print("\np:\t",p)
print("q:\t",q)

print("M:\t",M)
print("Seed:\t",seed)

x = seed

bit_output = ""
for _ in range(N):
    x = x*x % M
    b = x % 2
    bit_output += str(b)
# print(bit_output)
#
# print("\nNumber of zeros:\t",bit_output.count("0"))
#
# print("Number of ones:\t\t",bit_output.count("1"))

xi=''
len_range_num = int(input("Введите длину последовательности:"))

for i in range(1,len_range_num):
    val=pow(2,int(i),int(lcm(p-1,p-1)))
    xi += str(pow(int(seed),int(val),int(M)) %2)
print(xi)
write_txt(xi)


