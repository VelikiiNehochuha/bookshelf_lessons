#
#   Получаем сообщения из очереди (rabbitmq) и обрабатываем их
#
import os, sys
import sqlite3
import json

import pika
import requests

from utils import dict_factory


def search_book_at_shops(dshop, book):
    """ищем кингу в магазине"""
    requests.get(f'{dshop["base_url"]}{book["author"]} {book["name"]}')


def main():
    """слушаем очередь и на получение задания ищем книгу в интернет магазине"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='search_book')

    connection = sqlite3.connect('bookshelf_search_book.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("SELECT shops.* from shops limit 1;")
    shop = cursor.fetchone()
    connection.close()

    def callback_on_receive_book(ch, method, properties, body):
        search_book_at_shops(shop, json.loads(body))
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='search_book', on_message_callback=callback_on_receive_book, auto_ack=True)

    print(' [*] Ждем сообщений в очереди. Для выхода нажмите CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Исполнение прервано администратором')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)