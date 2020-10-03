-- создать таблицу
-- books_book definition
CREATE TABLE "books" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор в таблице
    "name" varchar(100) NOT NULL, -- поле название книги
    "author" varchar(100) NOT NULL, -- поле автор книги
    "pages" integer NOT NULL -- поле количество страниц
);

-- добавить запись в таблицу
INSERT INTO books (name, author, pages) values("Тихий дон", "Шолохов", 1000)

-- получить все записи из таблицы
SELECT * from books

-- получить одну удинственную запись по ID
SELECT * from books where id = 1 limit 1;

-- обновить запись в таблице
UPDATE books set pages = 1001 where id = 1;

-- удалить запись из таблицы

DELETE from books  where id = 1;


-- lesson 4
DROP TABLE "books";

CREATE TABLE "users" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор в таблице
    "email" varchar(255) NOT NULL UNIQUE, -- поле email
    "password" varchar(255) NOT NULL -- поле для пароля
);

CREATE TABLE "books" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор в таблице
    "name" varchar(100) NOT NULL, -- поле название книги
    "author" varchar(100) NOT NULL, -- поле автор книги
    "pages" integer NOT NULL, -- поле количество страниц
    "user_id" integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (email, password) values("admin@bookshelf.ru", "secret_password")


INSERT INTO books (name, author, pages, user_id) values("Тихий дон", "Шолохов", 1000, 1);

SELECT books.*, users.email from books JOIN users on users.id = books.user_id;

