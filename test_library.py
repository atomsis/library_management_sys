import unittest
from unittest.mock import patch, mock_open
from main import Book, Library  # Импортируйте Book и Library из main.py


class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Путь к тестовому файлу данных
        self.file_path = 'test_library.json'

    @patch('main.open', new_callable=mock_open, read_data='[]')
    def test_load_data_empty(self, mock_file):
        library = Library(self.file_path)
        self.assertEqual(library.books, [])

    @patch('main.open', new_callable=mock_open,
           read_data='[{"id": 1, "title": "Test Book", "author": "Test Author", "year": 2020, "status": "в наличии"}]')
    def test_load_data_with_books(self, mock_file):
        library = Library(self.file_path)
        self.assertEqual(len(library.books), 1)
        self.assertEqual(library.books[0].title, "Test Book")

    @patch('main.open', new_callable=mock_open, read_data='[]')
    @patch('main.Library.save_data')
    def test_add_book(self, mock_save, mock_file):
        file_path = 'test_file.json'
        mock_file.return_value = mock_open(read_data='[]').return_value

        library = Library(file_path)
        library.create_book("New Book", "New Author", 2021)
        self.assertEqual(len(library.books), 1)
        self.assertEqual(library.books[0].title, "New Book")

        mock_save.assert_called_once()

    @patch('main.open', new_callable=mock_open,
           read_data='[{"id": 1, "title": "Test Book", "author": "Test Author", "year": 2020, "status": "в наличии"}]')
    @patch('main.Library.save_data')
    def test_remove_book(self, mock_save, mock_file):
        library = Library(self.file_path)
        library.delete_book(1)
        self.assertEqual(len(library.books), 0)

    @patch('main.open', new_callable=mock_open,
           read_data='[{"id": 1, "title": "Test Book", "author": "Test Author", "year": 2020, "status": "в наличии"}]')
    def test_search_books(self, mock_file):
        library = Library(self.file_path)
        results = library.search_books("Test Book")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book")

    @patch('main.open', new_callable=mock_open,
           read_data='[{"id": 1, "title": "Test Book", "author": "Test Author", "year": 2020, "status": "в наличии"}]')
    @patch('main.Library.save_data')
    def test_change_status(self, mock_save, mock_file):
        library = Library(self.file_path)
        library.change_status(1, "выдана")
        self.assertEqual(library.books[0].status, "выдана")


if __name__ == '__main__':
    unittest.main()
