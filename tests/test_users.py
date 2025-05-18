"""
Тесты для проверки API пользователей:
регистрация, логин, обновление, удаление, ошибки и статистика.
"""
import unittest
from app import create_app
from app.extensions import db


class UserTestCase(unittest.TestCase):
    def setUp(self):
        """
        Создаёт тестовое приложение с базой в памяти
        """
        config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'PROPAGATE_EXCEPTIONS': True
        }
        self.app = create_app(config)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Очищает базу данных после каждого теста
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """
        Успешная регистрация
        """
        res = self.client.post('/users/register', json={
            'username': 'testuser',
            'email': 'test@mail.com',
            'password': '123456'
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('user_id', res.get_json())

    def test_login_success(self):
        """
        Успешный логин после регистрации
        """
        self.test_register_user()
        res = self.client.post('/users/login', json={
            'username': 'testuser',
            'password': '123456'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('user_id', res.get_json())

    def test_update_user(self):
        """
        Обновление существующего пользователя
        """
        reg = self.client.post('/users/register', json={
            'username': 'old',
            'email': 'old@mail.com',
            'password': '123'
        })
        user_id = reg.get_json()['user_id']
        res = self.client.put(f'/users/{user_id}', json={
            'username': 'new',
            'email': 'new@mail.com'
        })
        self.assertEqual(res.status_code, 200)
        get = self.client.get(f'/users/{user_id}')
        self.assertEqual(get.get_json()['username'], 'new')

    def test_delete_user(self):
        """
        Удаление пользователя
        """
        reg = self.client.post('/users/register', json={
            'username': 'delme',
            'email': 'del@mail.com',
            'password': 'abc'
        })
        user_id = reg.get_json()['user_id']
        res = self.client.delete(f'/users/{user_id}')
        self.assertEqual(res.status_code, 200)
        get = self.client.get(f'/users/{user_id}')
        self.assertEqual(get.status_code, 404)

    def test_register_missing_fields(self):
        """
        Пустой JSON
        """
        res = self.client.post('/users/register', json={})
        self.assertEqual(res.status_code, 400)

    def test_register_empty_password(self):
        """
        Пароль есть, но пустой
        """
        res = self.client.post('/users/register', json={
            'username': 'nopass',
            'email': 'no@mail.com',
            'password': ''
        })
        self.assertEqual(res.status_code, 400)

    def test_register_invalid_email(self):
        """
        Невалидный email
        """
        res = self.client.post('/users/register', json={
            'username': 'bademail',
            'email': 'not-an-email',
            'password': 'abc'
        })
        self.assertEqual(res.status_code, 400)

    def test_register_duplicate_user(self):
        """
        Повторная регистрация
        """
        self.test_register_user()
        res = self.client.post('/users/register', json={
            'username': 'testuser',
            'email': 'test@mail.com',
            'password': 'again'
        })
        self.assertEqual(res.status_code, 400)

    def test_login_missing_fields(self):
        """
        Логин без тела или с пустым телом
        """
        res = self.client.post('/users/login', json={})
        self.assertEqual(res.status_code, 400)

    def test_login_no_json(self):
        """
        Логин без JSON-заголовка
        """
        res = self.client.post('/users/login')
        self.assertEqual(res.status_code, 400)

    def test_login_wrong_password(self):
        """
        Неверный пароль у реального пользователя
        """
        self.test_register_user()
        res = self.client.post('/users/login', json={
            'username': 'testuser',
            'password': 'wrong'
        })
        self.assertEqual(res.status_code, 401)

    def test_update_nonexistent_user(self):
        """
        Попытка обновления несуществующего пользователя
        """
        res = self.client.put('/users/52', json={
            'username': 'ghost'
        })
        self.assertEqual(res.status_code, 404)

    def test_get_all_users(self):
        """
        Получение всех пользователей
        """
        self.client.post('/users/register', json={
            'username': 'user1',
            'email': 'u1@mail.com',
            'password': '123456'
        })
        self.client.post('/users/register', json={
            'username': 'user2',
            'email': 'u2@mail.com',
            'password': '123456'
        })
        res = self.client.get('/users/')
        self.assertEqual(res.status_code, 200)
        users = res.get_json()
        self.assertIsInstance(users, list)
        self.assertGreaterEqual(len(users), 2)

    def test_admin_stats(self):
        """
        Проверка статистики (пользователи, книги, обмены)
        """
        reg1 = self.client.post('/users/register', json={
            'username': 'user1',
            'email': 'user1@mail.com',
            'password': '52'
        })
        user1_id = reg1.get_json()['user_id']
        reg2 = self.client.post('/users/register', json={
            'username': 'user2',
            'email': 'user2@mail.com',
            'password': '48'
        })
        user2_id = reg2.get_json()['user_id']
        self.client.post('/books/', json={
            'title': 'Book 1',
            'author': 'Author A',
            'user_id': user1_id
        })
        self.client.post('/books/', json={
            'title': 'Book 2',
            'author': 'Author B',
            'user_id': user2_id
        })
        self.client.post('/exchange/', json={
            'sender_id': user1_id,
            'receiver_id': user2_id,
            'offered_book_id': 1,
            'requested_book_id': 2
        })
        res = self.client.get('/users/admin/stats')
        stats = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(stats['users'], 2)
        self.assertGreaterEqual(stats['books'], 2)
        self.assertGreaterEqual(stats['exchanges'], 1)


if __name__ == '__main__':
    unittest.main()
