import socket
import threading

class Server():

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 9096))
        self.server.listen(0)
        print("Server is listening")

    def listen_user(self,user):
            print("Listening user")

            while True:
                data = user.recv(2048)
                if data !=''.encode():
                    print(f"User send {data}")


    def start_server(self):  # старт сервера
            while True:
                user_socket, address = self.server.accept()  # принимаем входящее подключение
                print(f"User {address[0]} connected!") # добавляем users в массив

                # создаём дополнительные потоки для блокирующих функций
                # где args аргумент функции(неизменяемый список)
                listen_accepted_user = threading.Thread(
                    target=self.listen_user,
                    args=(user_socket,)
                    )

                listen_accepted_user.start()  # запуск дополнительного потока


if __name__ == '__main__':
   Serv = Server()
   Serv.start_server()
