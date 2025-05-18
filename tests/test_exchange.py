"""
Тесты для проверки API обменов: создание, получение,
обновление статуса, ошибки и получение списка обменов.
"""
import unittest
from app import create_app
from app.extensions import db
from app.models import User, Book


class ExchangeTestCase(unittest.TestCase):
    def setUp(self):
        """
        Создаёт тестовое приложение, пользователей и книги для обмена
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
            user1 = User(username='u1', email='u1@mail.com',
                         password_hash='h1', role='user')
            user2 = User(username='u2', email='u2@mail.com',
                         password_hash='h2', role='user')
            db.session.add_all([user1, user2])
            db.session.commit()
            self.user1_id = user1.id
            self.user2_id = user2.id
            book1 = Book(title='Book 1', author='Author A', user_id=user1.id)
            book2 = Book(title='Book 2', author='Author B', user_id=user2.id)
            db.session.add_all([book1, book2])
            db.session.commit()
            self.book1_id = book1.id
            self.book2_id = book2.id

    def tearDown(self):
        """
        Очищает базу данных после каждого теста
        """
        with self.app.app_context():
            db.drop_all()

    def test_create_exchange(self):
        """
        Успешное предложение обмена
        """
        res = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'receiver_id': self.user2_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('exchange_id', res.get_json())

    def test_duplicate_pending_exchange(self):
        """
        Повторное предложение обмена с теми же книгами должно вернуть 400
        """
        self.test_create_exchange()
        res = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'receiver_id': self.user2_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        self.assertEqual(res.status_code, 400)

    def test_get_exchange_by_id(self):
        """
        Получить обмен по ID
        """
        create = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'receiver_id': self.user2_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        exchange_id = create.get_json()['exchange_id']
        res = self.client.get(f'/exchange/{exchange_id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['status'], 'pending')

    def test_update_exchange_status(self):
        """
        Проверяем успешное обновление на 'accepted'
        """
        create = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'receiver_id': self.user2_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        exchange_id = create.get_json()['exchange_id']
        res = self.client.patch(f'/exchange/{exchange_id}',
                                json={'status': 'accepted'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Статус обновлён', res.get_json()['message'])

    def test_update_exchange_invalid_status(self):
        """
        Неверный статус — ошибка
        """
        create = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'receiver_id': self.user2_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        exchange_id = create.get_json()['exchange_id']
        res = self.client.patch(f'/exchange/{exchange_id}',
                                json={'status': 'abaudna'})
        self.assertEqual(res.status_code, 400)

    def test_update_nonexistent_exchange(self):
        """
        Обновление несуществующего обмена
        """
        res = self.client.patch('/exchange/52', json={'status': 'accepted'})
        self.assertEqual(res.status_code, 404)

    def test_get_user_exchanges(self):
        """
        Получение всех обменов пользователя
        """
        self.test_create_exchange()
        res = self.client.get(f'/exchange/user/{self.user1_id}')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.get_json()), 1)

    def test_get_all_exchanges(self):
        """
        Получить все обмены
        """
        self.test_create_exchange()
        res = self.client.get('/exchange/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
        self.assertGreaterEqual(len(res.get_json()), 1)

    def test_exchange_missing_fields(self):
        """
        Пропущено обязательное поле
        """
        res = self.client.post('/exchange/', json={
            'sender_id': self.user1_id,
            'offered_book_id': self.book1_id,
            'requested_book_id': self.book2_id
        })
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
