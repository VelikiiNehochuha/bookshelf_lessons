#
#   Получаем сообщения из очереди (rabbitmq) и обрабатываем их
#
import os
import sys
import sqlite3
import json
import datetime

import structlog
import pika
import requests
from bs4 import BeautifulSoup

from utils import dict_factory


logger = structlog.getLogger()


def search_book_at_shops(dshop, book):
    """ищем кингу в магазине"""

    url = f'{dshop["base_url"]}{book["name"].replace(" ", "+")}+{book["author"].replace(" ", "+")}'
    print(url)
    response = requests.get(url)
    html_doc = response.text
    # print(html_doc)

    soup = BeautifulSoup(html_doc, 'html.parser')
    search_results = soup.find(id="searchresults")
    print(search_results)
    first_result = search_results.find("div", {"class": "search__item"})
    cover = first_result.find("div", {"class": "cover"})
    raw_data = cover.get("data-obj")
    raw_params = raw_data.strip('{').strip('}').split(',')
    params = {}
    for raw_param in raw_params:
        name_value = raw_param.split(':')
        params[name_value[0]] = name_value[1].strip().strip("'")
    available = params.get("available", "")
    price = params.get("price", "")
    if available and available == "1":
        is_available = True
    else:
        is_available = False
    if price:
        price = int(100 * float(price))
    else:
        price = None
    return {
        "is_available": is_available,
        "price": price
    }


def callback_on_search_book(ch, method, properties, body):
    logger.info(body)
    json_body = json.loads(body)

    # книга доступна нужно сохранить результаты в бд
    db_conn = sqlite3.connect('bookshelf_search_book.db')
    db_conn.row_factory = dict_factory
    cursor = db_conn.cursor()
    cursor.execute("SELECT * from books where name = ? and author = ? limit 1", [json_body["name"], json_body["author"]])
    exist_book = cursor.fetchone()
    cursor.execute("SELECT shops.* from shops limit 1;")
    shop = cursor.fetchone()
    db_conn.close()

    result = search_book_at_shops(shop, json_body)
    if not result["is_available"]:
        logger.info(result)
        return
    db_conn = sqlite3.connect('bookshelf_search_book.db')
    if not exist_book:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO books (name, author) values(?, ?);",
                       [json_body["name"], json_body["author"]])
        cursor.execute("SELECT last_insert_rowid() from books;")
        book_id = cursor.fetchone()[0]
    else:
        book_id = exist_book["id"]
    cursor.execute("INSERT INTO books_to_shops (shop_id, book_id, price, from_datetime) values(?, ?, ?, ?);",
                   [shop["id"], book_id, result["price"], datetime.datetime.now()])
    db_conn.commit()
    db_conn.close()
    logger.info("Добавлен результат поиска книги в магазине в базу данных микросервиса")


def main():
    """слушаем очередь и на получение задания ищем книгу в интернет магазине"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='search_book')
    channel.basic_consume(queue='search_book', on_message_callback=callback_on_search_book, auto_ack=True)
    logger.info(' [*] Ждем сообщений в очереди. Для выхода нажмите CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Исполнение прервано администратором')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)