import sqlite3


if __name__ == "__main__":
    # создать базу данных для сайта bookshelf
    conn = sqlite3.connect('bookshelf.db')

    # создать базу данных для микросервиса поиск книги
    conn_2 = sqlite3.connect('bookshelf_search_book.db')
