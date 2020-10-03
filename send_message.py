__all__ = [
    "send_message_to_search_book"
]
import json


import zmq


context = zmq.Context()
socket = context.socket(zmq.REQ)


def send_message_to_search_book(payload):
    try:
        print(payload)
        socket.connect("tcp://localhost:5555")
        socket.send_string(json.dumps(payload))
        print("Успешно отправили сообщение в мироксервис search book")
        message = socket.recv()
        print(message)
    except Exception as e:
        print(e)
        print("Микросервис search book не доступен")