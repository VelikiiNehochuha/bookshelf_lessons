__all__ = [
    "send_message_to_search_book"
]
import json


import pika



def send_message_to_search_book(payload):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=json.dumps(payload))
        connection.close()
        print("Успешно отправили сообщение в мироксервис search book")
    except Exception as e:
        print(e)
        print("Микросервис search book не доступен")