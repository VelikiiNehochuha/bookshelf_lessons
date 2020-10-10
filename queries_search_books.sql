-- стурктура таблиц для микросервиса search_book

CREATE TABLE "shops" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор в таблице
    "base_url" varchar(255) NOT NULL, -- базовый URL адрес магазина
    "name" varchar(255) NOT NULL -- название магазина
);

CREATE TABLE "books" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор в таблице
    "name" varchar(100) NOT NULL, -- поле название книги
    "author" varchar(100) NOT NULL -- поле автор книги
);

CREATE TABLE "books_to_shops" (
    from_datetime datetime NOT NULL,
    price  integer,
    "shop_id" integer NOT NULL,
    "book_id" integer NOT NULL,
    FOREIGN KEY (shop_id) REFERENCES shops(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

INSERT INTO books (name, author) values('Тихий дон', 'Шолохов');
INSERT INTO books (name, author) values('Записки молодого врача', 'Булгаков');

INSERT  INTO shops (base_url, name) values('https://www.litres.ru/pages/rmd_search/?q=', 'Литрес');


SELECT shops.name from shops join books_to_shops on books_to_shops.shop_id = shops.id join books on books_to_shops.book_id = books.id WHERE
books.name = 'Тихий дон';


INSERT INTO books_to_shops (book_id, shop_id, from_datetime) values(1, 1, '2020-09-26 17:00:00');