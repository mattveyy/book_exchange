"""
Модели базы данных для пользователей, книг и обменов.
"""
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Модель пользователя: хранит имя, email, хэш пароля, роль, связи с книгами
    и обменами.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user')

    books = db.relationship('Book', backref='owner', lazy=True)
    sent_exchanges = db.relationship(
        'Exchange',
        foreign_keys='Exchange.sender_id',
        backref='sender_user'
    )
    received_exchanges = db.relationship(
        'Exchange',
        foreign_keys='Exchange.receiver_id',
        backref='receiver_user'
    )

    def set_password(self, password):
        """Установка хэша пароля."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Проверка пароля."""
        return check_password_hash(self.password_hash, password)


class Book(db.Model):
    """
    Модель книги: название, автор, жанр, описание, местоположение, статус,
    владелец.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(80))
    description = db.Column(db.Text)
    location = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='available')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Exchange(db.Model):
    """
    Модель обмена: отправитель, получатель, книги, статус, время создания.
    """
    __tablename__ = 'exchanges'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=False)
    offered_book_id = db.Column(db.Integer, db.ForeignKey('books.id'),
                                nullable=False)
    requested_book_id = db.Column(db.Integer, db.ForeignKey('books.id'),
                                  nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    offered_book = db.relationship('Book', foreign_keys=[offered_book_id])
    requested_book = db.relationship('Book', foreign_keys=[requested_book_id])
