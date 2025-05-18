"""
Тесты для проверки API книг: создание, получение, обновление,
удаление, фильтрация и обработка ошибок.
"""
import unittest
from app import create_app
from app.extensions import db
from app.models import User


class BookTestCase(unittest.TestCase):
    def setUp(self):
        """
        Настраиваем тестовое приложение с SQLite в памяти
        """
        config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        self.app = create_app(config)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.user = User(username='user1', email='user1@mail.com',
                             password_hash='hashed', role='user')
            db.session.add(self.user)
            db.session.commit()
            self.user_id = self.user.id

    def tearDown(self):
        """
        Очищаем базу данных после каждого теста
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_book(self):
        """
        Успешное добавление книги
        """
        res = self.client.post('/books/', json={
            'title': '1984',
            'author': 'Orwell',
            'user_id': self.user_id
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('book_id', res.get_json())

    def test_get_book_by_id(self):
        """
        Получение книги по ID
        """
        self.test_create_book()
        res = self.client.get('/books/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['title'], '1984')

    def test_update_book(self):
        """
        Обновление информации о книге
        """
        self.test_create_book()
        res = self.client.put('/books/1', json={'title': 'Animal Farm'})
        self.assertEqual(res.status_code, 200)
        updated = self.client.get('/books/1').get_json()
        self.assertEqual(updated['title'], 'Animal Farm')

    def test_delete_book(self):
        """
        Удаление книги
        """
        self.test_create_book()
        res = self.client.delete('/books/1')
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/books/1')
        self.assertEqual(res.status_code, 404)

    def test_filter_books(self):
        """
        Фильтрация по автору
        """
        self.test_create_book()
        res = self.client.get('/books/?author=Orwell')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.get_json()), 1)

    def test_create_book_missing_fields(self):
        """
        Пропущены обязательные поля
        """
        res = self.client.post('/books/', json={
            'title': 'No Author'
        })
        self.assertEqual(res.status_code, 400)

    def test_create_book_empty_title(self):
        """
        Поле title есть, но пустое
        """
        res = self.client.post('/books/', json={
            'title': '',
            'author': 'Somebody',
            'user_id': self.user_id
        })
        self.assertEqual(res.status_code, 400)

    def test_get_nonexistent_book(self):
        """
        Книга с таким ID не существует
        """
        res = self.client.get('/books/52')
        self.assertEqual(res.status_code, 404)

    def test_update_nonexistent_book(self):
        """
        Попытка обновить несуществующую книгу
        """
        res = self.client.put('/books/52', json={'title': 'Ghost'})
        self.assertEqual(res.status_code, 404)

    def test_delete_nonexistent_book(self):
        """
        Попытка удалить несуществующую книгу
        """
        res = self.client.delete('/books/52')
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
