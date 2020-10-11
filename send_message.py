__all__ = [
    "send_message_to_search_book"
]

import json

import structlog
import pika

logger = structlog.getLogger()


def send_message_to_search_book(payload):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="search_book")
        logger.info(payload)
        channel.basic_publish(exchange='',
                              routing_key='search_book',
                              body=json.dumps(payload))
        connection.close()
        logger.info("Успешно отправили сообщение в мироксервис search book")
    except Exception as e:
        logger.error(e)
        logger.error("Микросервис search book не доступен")
