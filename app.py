import sqlite3

from flask import Flask, render_template, request, jsonify
import structlog

from utils import dict_factory
from send_message import send_message_to_search_book, get_search_results


app = Flask("bookshelf")
logger = structlog.getLogger()


@app.route('/')
def homepage():
    return render_template('index.html')


# По url адресу /api/books мы должны уметь получать список книг и создавать книгу
@app.route('/api/books', methods=["GET", "POST"])  # https://pythonbasics.org/flask-tutorial-routes/
def api_books():
    if request.method == "GET":
        """Получить список книг"""
        connection = sqlite3.connect('bookshelf.db')
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT books.*, users.email from books JOIN users on users.id = books.user_id;")
        db_results = cursor.fetchall()
        connection.close()
        results = list()
        for result in db_results:
            results.append({
                "id": result["id"],
                "name": result["name"],
                "author": result["author"],
                "pages": result["pages"],
                "user_email": result["email"]
            })
        return jsonify({"results": results})
    if request.method == "POST":
        """Добавить книгу"""
        payload = request.get_json()
        logger.info(payload)
        # работа с базой данных
        connection = sqlite3.connect('bookshelf.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (name, author, pages, user_id) values(?, ?, ?, ?);",
                       [payload["name"], payload["author"], payload["pages"], 1])  # 1 это id пользователя в базе
        cursor.execute("SELECT last_insert_rowid() from books;")
        book_id = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        logger.info(book_id)
        send_message_to_search_book({
            "name": payload["name"],
            "author": payload["author"]
        })
        return jsonify({
            "id": book_id,
            "name": payload["name"],
            "author": payload["author"],
            "pages": payload["pages"]
        })
    assert False, "Нет такой операции"


# По url адресу /api/books/<book_id> мы должны уметь получать конкретную книгу, обновлять и удалять её
@app.route('/api/books/<book_id>', methods=["GET", "PUT", "DELETE"])
def api_books_item():
    if request.method == "PUT":
        """Обновить книгу"""
    if request.method == "GET":
        """Получить книгу"""
    if request.method == "DELETE":
        """Удалить книгу"""
    assert False, "Нет такой операции"


@app.route('/api/search-results/<book_id>', methods=["GET"])
def search_results(book_id):
    """обращение к микросервису поиска книг за результами поиска книги"""
    connection = sqlite3.connect('bookshelf.db', check_same_thread=False)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("SELECT books.* from books WHERE id = ?;", [book_id])
    book = cursor.fetchone()
    connection.close()
    # в данном методое мы не только отправляем запрос в микросервис но и ждем резулльтата его обработки,
    # таким образом мы можем сразу получить результат прямо в REST API
    response = get_search_results({
        "name": book["name"],
        "author": book["author"]
    }, book_id)
    logger.debug(response)
    return jsonify({"results": response or []})



app.run(debug=True)  # запуск сервера
