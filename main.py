# 📚 Шаблон для практического задания
# Тема: Работа с базами данных в Python с использованием SQLite (DB API 2.0)
# Задание: Реализовать простую библиотечную систему

import sqlite3
from datetime import date

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 📌 Функция создания таблиц
def create_tables():
    """
    Создай три таблицы: Books, Users, Borrowings.
    Используй CREATE TABLE IF NOT EXISTS и укажи типы данных.
    Не забудь задать первичные ключи и связи (FOREIGN KEY).
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                      id INTEGER PRIMARY KEY,
                      title TEXT NOT NULL,
                      author TEXT NOT NULL,
                      year INTEGER,
                      available BOOLEAN DEFAULT TRUE)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Borrowings (
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER NOT NULL,
                      book_id INTEGER NOT NULL,
                      borrow_date DATE NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES Users(id),
                      FOREIGN KEY (book_id) REFERENCES Books(id))''')
    conn.commit()

# 📌 Функция заполнения базы начальными данными
def seed_data():
    """
    Вставь в таблицы Books и Users несколько строк с начальными данными.
    Используй executemany() и параметризованные запросы (?).
    """
    books_data = [
        ('Война и мир', 'Лев Толстой', 1869, True),
        ('Преступление и наказание', 'Федор Достоевский', 1866, True),
        ('Продавец воздуха', 'Беляев', 1949, True),
        ('Мастер и Маргарита', 'Михаил Булгаков', 1967, True),
        ('Голова профессора Доуэля', 'Беляев', 1997, True)
    ]
    
    users_data = [
        ('Иван Иванов', 'ivan@example.com'),
        ('Петр Петров', 'petr@example.com'),
        ('Сергей Сергеев', 'sergey@example.com')
    ]
    
    cursor.executemany('INSERT INTO Books (title, author, year, available) VALUES (?, ?, ?, ?)', books_data)
    cursor.executemany('INSERT INTO Users (name, email) VALUES (?, ?)', users_data)
    conn.commit()
    print("✅ Начальные данные успешно добавлены")

# 📌 Функция выдачи книги
def borrow_book(user_id, book_id):
    """
    Проверь, доступна ли книга.
    Если да — выдай её (обнови поле available в Books и создай запись в Borrowings).
    Обработай возможные ошибки (например, книга уже выдана).
    """
    try:
        cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            print(f"❌ Пользователь с ID {user_id} не найден")
            return
        
        cursor.execute('SELECT available FROM Books WHERE id = ? AND available = TRUE', (book_id,))
        book = cursor.fetchone()
        
        if not book:
            print(f"❌ Книга с ID {book_id} не найдена")
            return
            
        if not book[0]:
            print(f"❌ Книга с ID {book_id} уже выдана")
            return
            
        cursor.execute('UPDATE Books SET available = FALSE WHERE id = ?', (book_id,))
        cursor.execute('INSERT INTO Borrowings (user_id, book_id, borrow_date) VALUES (?, ?, ?)', 
                      (user_id, book_id, date.today()))
        conn.commit()
        print(f"✅ Книга с ID {book_id} успешно выдана пользователю с ID {user_id}")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при выдаче книги: {e}")

# 📌 Функция возврата книги
def return_book(book_id):
    """
    Отметь книгу как доступную.
    Проверь, что она действительно была выдана.
    """
    try:
        cursor.execute('SELECT available FROM Books WHERE id = ? AND available = FALSE', (book_id,))
        book = cursor.fetchone()
        
        if not book:
            print(f"❌ Книга с ID {book_id} не найдена")
            return
            
        if book[0]:
            print(f"❌ Книга с ID {book_id} уже доступна (не была выдана)")
            return
            
        cursor.execute('UPDATE Books SET available = TRUE WHERE id = ?', (book_id,))
        cursor.execute('DELETE FROM Borrowings WHERE book_id = ?', (book_id,))
        conn.commit()
        print(f"✅ Книга с ID {book_id} успешно возвращена")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при возврате книги: {e}")

# 📌 Функция отображения всех книг
def show_books():
    """
    Выведи список всех книг с их статусом: 'Доступна' или 'Выдана'.
    """
    try:
        cursor.execute('''SELECT id, title, author, year, 
                         CASE WHEN available THEN 'Доступна' ELSE 'Выдана' END as status 
                         FROM Books''')
        books = cursor.fetchall()
        
        if not books:
            print("❌ В библиотеке нет книг")
            return
            
        print("\n📚 Список всех книг:")
        print("{:<5} {:<40} {:<25} {:<8} {:<10}".format(
            "ID", "Название", "Автор", "Год", "Статус"))
        print("-" * 90)
        for book in books:
            print("{:<5} {:<40} {:<25} {:<8} {:<10}".format(*book))
    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении списка книг: {e}")

# 📌 Функция отображения всех пользователей
def show_users():
    """
    Выведи список всех пользователей библиотеки.
    """
    try:
        cursor.execute('''SELECT id, name, email FROM Users''')
        users = cursor.fetchall()
        
        if not users:
            print("❌ В библиотеке нет зарегистрированных пользователей")
            return
            
        print("\n👥 Список всех пользователей:")
        print("{:<5} {:<30} {:<30}".format(
            "ID", "Имя", "Email"))
        print("-" * 70)
        for user in users:
            print("{:<5} {:<30} {:<30}".format(*user))
    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении списка пользователей: {e}")

# 📌 Функция показа книг, выданных конкретному пользователю
def show_user_books(user_id):
    """
    Выведи список книг, которые на руках у пользователя.
    Используй JOIN между Borrowings и Books.
    """
    try:
        cursor.execute('''SELECT b.id, b.title, b.author, br.borrow_date 
                         FROM Books b
                         JOIN Borrowings br ON b.id = br.book_id
                         WHERE br.user_id = ?''', (user_id,))
        books = cursor.fetchall()
        
        if not books:
            print(f"❌ У пользователя с ID {user_id} нет выданных книг")
            return
            
        print(f"\n📚 Книги пользователя с ID {user_id}:")
        print("{:<5} {:<40} {:<25} {:<12}".format(
            "ID", "Название", "Автор", "Дата выдачи"))
        print("-" * 85)
        for book in books:
            print("{:<5} {:<40} {:<25} {:<12}".format(*book))
    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении списка книг пользователя: {e}")

# 📌 Функция поиска книг по ключевому слову (нечувствительна к регистру)
def search_books(keyword):
    """
    Найди книги по названию или автору.
    Используй LIKE и подстановку (%ключевое_слово%).
    """
    try:
        # Создаем регулярное выражение для нечувствительного к регистру поиска
        regex_pattern = f"(?i){keyword}"
        
        # Включаем поддержку REGEXP в SQLite
        def regexp(expr, item):
            import re
            return re.search(expr, item, re.IGNORECASE) is not None
        
        conn.create_function("REGEXP", 2, regexp)
        
        cursor.execute('''SELECT id, title, author, year, 
                         CASE WHEN available THEN 'Доступна' ELSE 'Выдана' END as status 
                         FROM Books 
                         WHERE title REGEXP ? OR author REGEXP ?''', 
                      (regex_pattern, regex_pattern))
        books = cursor.fetchall()
        
        if not books:
            print(f"❌ Книги по запросу '{keyword}' не найдены")
            return
            
        print(f"\n🔍 Результаты поиска по запросу '{keyword}':")
        print("{:<5} {:<40} {:<25} {:<8} {:<10}".format(
            "ID", "Название", "Автор", "Год", "Статус"))
        print("-" * 90)
        for book in books:
            print("{:<5} {:<40} {:<25} {:<8} {:<10}".format(*book))
    except sqlite3.Error as e:
        print(f"❌ Ошибка при поиске книг: {e}")
# 📌 Функция добавления нового пользователя
def add_user(name, email):
    """
    Вставь нового пользователя в таблицу Users.
    Обработай исключение, если email уже есть в базе.
    """
    try:
        cursor.execute('INSERT INTO Users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        print(f"✅ Пользователь {name} успешно добавлен")
    except sqlite3.IntegrityError:
        print(f"❌ Пользователь с email {email} уже существует")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при добавлении пользователя: {e}")

# 🧭 Главное меню приложения
def main_menu():
    """
    Обеспечивает взаимодействие с пользователем через консольное меню.
    """
    while True:
        print("\n📚 Главное меню:")
        print("1. Показать все книги")
        print("2. Показать всех пользователей")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Показать книги пользователя")
        print("6. Поиск книги")
        print("7. Добавить пользователя")
        print("8. Наполнить таблицу данными")
        print("9. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            show_books()
        elif choice == '2':
            show_users()
        elif choice == '3':
            try:
                show_users()
                user_id = int(input("ID пользователя: "))
                show_books()
                book_id = int(input("ID книги: "))
                borrow_book(user_id, book_id)
            except ValueError:
                print("❌ Введите корректные числа.")
        elif choice == '4':
            try:
                show_books()
                book_id = int(input("ID книги для возврата: "))
                return_book(book_id)
            except ValueError:
                print("❌ Введите корректный ID.")
        elif choice == '5':
            try:
                user_id = int(input("ID пользователя: "))
                show_user_books(user_id)
            except ValueError:
                print("❌ Введите корректный ID.")
        elif choice == '6':
            keyword = input("Введите слово для поиска: ")
            search_books(keyword)
        elif choice == '7':
            show_users()
            name = input("Имя пользователя: ")
            email = input("Email пользователя: ")
            add_user(name, email)
        elif choice == '8':
            seed_data()
            print("Данные заполнены!")
        elif choice == '9':
            print("👋 До свидания!")
            break
        else:
            print("⚠️ Некорректный выбор. Попробуйте снова.")

        input('Для продолжения нажмите любую клавишу...')

# ▶️ Запуск приложения
if __name__ == '__main__':
    create_tables()
    # seed_data()  # Раскомментируй один раз для заполнения начальными данными
    main_menu()
    conn.close()