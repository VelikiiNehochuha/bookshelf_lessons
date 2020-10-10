__all__ = [
    "send_message_to_search_book",
    "get_search_results"
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


def get_search_results(book, user_id):
    # отправляем запрос на получение результатов
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="get_search_results")
        payload = {
            "book": book,
            "user_id": user_id
        }
        logger.info(payload)
        channel.basic_publish(exchange='',
                              routing_key='get_search_results',
                              body=json.dumps(payload))
        logger.info("Успешно отправили сообщение в мироксервис search book на получение результатов")
    except Exception as e:
        logger.error(e)
        return
    # ждем ответа от сервиса
    channel.queue_declare(queue=f'get_search_results_{user_id}')

    search_results = []

    for _, _, body in channel.consume(queue=f'get_search_results_{user_id}', auto_ack=True, inactivity_timeout=10):
        if not body:
            continue
        search_results = json.loads(body)
        break
    print(search_results)
    connection.close()
    return search_results
