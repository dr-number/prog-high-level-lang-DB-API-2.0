# Ларионов гр. 410з. Программирование на языках высокого уровня
# Тема 3. Модульное программирование. ПЗ DB API 2.0
Тема: Работа с базами данных в Python с использованием SQLite (DB API 2.0)
Задание: Реализовать простую библиотечную систему

## Заполнение и просмотр данных
<figure>
   <p align="center">Заполнение данными</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/0-seed-data.png">
   </p>
</figure>
<figure>
   <p align="center">Просмотр всех пользователей</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/0-show-users.png">
   </p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/1-show-all-users.png">
   </p>
</figure>
<figure>
   <p align="center">Нет книг</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/0-no-books.png">
   </p>
</figure>
<figure>
   <p align="center">Просмотр всех книг</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/0-show-books.png">
   </p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/1-show-all-books.png">
   </p>
</figure>
<figure>
   <p align="center">Ошибка выбора</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/0-error-select.png">
   </p>
</figure>

## Выдача книг
<figure>
   <p align="center">Выдача книги пользователю</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/3-borrow_book.png">
   </p>
</figure>
<figure>
   <p align="center">Книга не найдена</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/3-book-not-found.png">
   </p>
</figure>
<figure>
   <p align="center">Книга уже выдана</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/3-borrow_book-already_borrow.png">
   </p>
</figure>
<figure>
   <p align="center">Некорректный выбор пользователя</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/3-error-value-1.png">
   </p>
</figure>
<figure>
   <p align="center">Некорректный выбор книги</p>
   <p align="center">
      <img src="https://github.com/dr-number/prog-high-level-lang-DB-API-2.0/blob/main/for_read_me/3-error-value-2.png">
   </p>
</figure>


# Create venv:
    python3 -m venv venv

# Activate venv:
## In Windows:
    venv\Scripts\activate
     
## In macOS or Linux:
    source venv/bin/activate

# start 
    ./venv/bin/python "main.py"
