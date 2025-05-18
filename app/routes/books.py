"""
Маршруты для работы с книгами: создание, получение, обновление, удаление,
фильтрация.
"""
from flask import Blueprint, request, jsonify
from app.models import Book
from app.extensions import db
from datetime import datetime
from app.models import Exchange

books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/', methods=['GET'])
def get_books():
    """
    Получить список книг с возможностью фильтрации и сортировки.
    """
    query = Book.query

    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')
    location = request.args.get('location')
    status = request.args.get('status')
    sort_by = request.args.get('sort')

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if location:
        query = query.filter(Book.location.ilike(f"%{location}%"))
    if status:
        query = query.filter(Book.status == status)

    if sort_by == 'created_at':
        query = query.order_by(Book.created_at.desc())
    elif sort_by == 'title':
        query = query.order_by(Book.title.asc())

    books = query.all()
    return jsonify([
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'description': book.description,
            'location': book.location,
            'created_at': book.created_at.isoformat(),
            'status': book.status,
            'user_id': book.user_id
        }
        for book in books
    ])


@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Получить книгу по её ID.
    """
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Книга не найдена'}), 404

    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'description': book.description,
        'location': book.location,
        'created_at': book.created_at.isoformat(),
        'status': book.status,
        'user_id': book.user_id
    })


@books_bp.route('/', methods=['POST'])
def add_book():
    """
    Добавить новую книгу.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Ожидаются данные в формате JSON'}), 400

    required_fields = ['title', 'author', 'user_id']
    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({
                'error': f'Поле "{field}" обязательно и не может быть пустым'
            }), 400

    try:
        user_id = int(data['user_id'])
    except ValueError:
        return jsonify({'error': 'user_id должен быть целым числом'}), 400

    book = Book(
        title=data['title'].strip(),
        author=data['author'].strip(),
        genre=data.get('genre'),
        description=data.get('description'),
        location=data.get('location'),
        user_id=user_id,
        status='available',
        created_at=datetime.utcnow()
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Книга добавлена', 'book_id': book.id}), 201


@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Обновить информацию о книге по её ID.
    """
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Книга не найдена'}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.description = data.get('description', book.description)
    book.location = data.get('location', book.location)
    book.status = data.get('status', book.status)

    db.session.commit()

    return jsonify({'message': 'Книга обновлена'})


@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Удалить книгу по её ID и связанные с ней обмены.
    """
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Книга не найдена'}), 404

    try:
        Exchange.query.filter(
            (Exchange.offered_book_id == book_id) |
            (Exchange.requested_book_id == book_id)
        ).delete(synchronize_session=False)

        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Книга удалена'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка удаления: {e}'}), 500
