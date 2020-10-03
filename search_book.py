#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Микросервис поиска книг в магазине запущен")

while True:
    message = socket.recv()
    print("Получили запрос на поиск книги в магазинах request: %s" % message)
    socket.send(b"Ok")

    #  Тут нужно написать функцию по поиску книги в магазине и сохранение результатов в базе данных
    time.sleep(1)