"""
Маршруты для работы с пользователями: регистрация, логин,
обновление, удаление, получение, статистика.
"""
from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Book, Exchange
import re

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/register', methods=['POST'])
def register():
    """
    Зарегистрировать нового пользователя.
    """
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not \
            data.get('password'):
        return jsonify({'error': 'Все поля обязательны'}), 400

    email_type = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_type, data['email']):
        return jsonify({'error': 'Некорректный email'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'error': 'Пользователь с таким именем уже существует'
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Почта уже используется'}), 400

    password_hash = generate_password_hash(
        data['password'],
        method='pbkdf2:sha256'
    )

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role='user'
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Регистрация успешна',
        'user_id': user.id
    }), 201


@users_bp.route('/login', methods=['POST'])
def login():
    """
    Авторизовать пользователя по имени и паролю.
    """
    if not request.is_json:
        return jsonify({'error': 'Ожидается JSON'}), 400

    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Все поля обязательны'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password_hash,
                                           data['password']):
        return jsonify({
            'error': 'Неверное имя пользователя или пароль'
        }), 401

    return jsonify({
        'message': 'Вход выполнен',
        'user_id': user.id,
        'role': user.role
    })


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Получить пользователя по его ID.
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Обновить данные пользователя по его ID.
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])

    db.session.commit()

    return jsonify({'message': 'Данные пользователя обновлены'})


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Удалить пользователя по его ID.
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'Пользователь с id={user_id} удалён'})


@users_bp.route('/', methods=['GET'])
def list_users():
    """
    Получить список всех пользователей.
    """
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        for user in users
    ])


@users_bp.route('/admin/stats', methods=['GET'])
def admin_stats():
    """
    Получить статистику по пользователям, книгам и обменам.
    """
    total_users = User.query.count()
    total_books = Book.query.count()
    total_exchanges = Exchange.query.count()

    return jsonify({
        'users': total_users,
        'books': total_books,
        'exchanges': total_exchanges
    })
