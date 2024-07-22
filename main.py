import json
from typing import List, Dict, Any

class Book:
    """
    Класс, представляющий книгу.
    """
    def __init__(self, id: int, title: str, author: str, year: int, status: str):
        """
        Инициализирует объект Book с указанными атрибутами.

        Параметры:
            id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги.
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

class Library:
    """
    Класс, представляющий библиотеку.

    Атрибуты:
        file_path (str): Путь к файлу, где хранятся данные о книгах.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, file_path: str):
        """
        Инициализирует объект Library и загружает данные из файла.

        Параметры:
            file_path (str): Путь к файлу с данными о книгах.
        """
        self.file_path = file_path
        self.books: List[Book] = self.load_data()

    def load_data(self) -> List[Book]:
        """
        Загружает данные о книгах из файла JSON и возвращает список объектов Book.

        Возвращает:
            List[Book]: Список объектов Book, загруженных из файла.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        return [Book(**book) for book in books_data]

    def save_data(self):
        """
        Сохраняет текущий список книг в файл JSON.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def create_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        Параметры:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        new_id = max(book.id for book in self.books) + 1 if self.books else 1
        new_book = Book(id=new_id, title=title, author=author, year=year, status='в наличии')
        self.books.append(new_book)
        self.save_data()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def delete_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки по её идентификатору.

        Параметры:
            book_id (int): Идентификатор книги, которую нужно удалить.
        """
        self.books = [book for book in self.books if book.id != book_id]
        self.save_data()
        print(f"Книга с ID {book_id} удалена из библиотеки.")

    def search_books(self, query: str) -> List[Book]:
        """
        Ищет книги по названию, автору или году издания.

        Параметры:
            query (str): Поисковый запрос (название, автор или год).

        Возвращает:
            List[Book]: Список книг, соответствующих запросу.
        """
        results = [book for book in self.books if
                   query.lower() in book.title.lower() or
                   query.lower() in book.author.lower() or
                   str(query) == str(book.year)]
        return results

    def change_status(self, book_id: int, status: str):
        """
        Изменяет статус книги по её идентификатору.

        Параметры:
            book_id (int): Идентификатор книги, статус которой нужно изменить.
            status (str): Новый статус книги.
        """
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_data()
                print(f"Статус книги с ID {book_id} изменен на '{status}'.")
                break
        else:
            print(f"Книга с ID {book_id} не найдена.")
