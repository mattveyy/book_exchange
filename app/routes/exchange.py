"""
Маршруты для работы с обменами книг: создание, получение, обновление статуса,
получение списка обменов.
"""
from flask import Blueprint, request, jsonify
from app.models import Exchange
from app.extensions import db
from datetime import datetime
from app.models import Book

exchange_bp = Blueprint('exchange', __name__, url_prefix='/exchange')


@exchange_bp.route('/', methods=['POST'])
def propose_exchange():
    """
    Предложить новый обмен книгами между пользователями.
    """
    data = request.get_json()

    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        offered_book_id = data['offered_book_id']
        requested_book_id = data['requested_book_id']

        offered_book = Book.query.get(offered_book_id)
        if not offered_book or offered_book.user_id != sender_id:
            return jsonify({
                'error': 'Книга не принадлежит отправителю'
            }), 400

        requested_book = Book.query.get(requested_book_id)
        if not requested_book:
            return jsonify({
                'error': 'Запрашиваемая книга не найдена'
            }), 400

        if (offered_book.status != 'available' or
                requested_book.status != 'available'):
            return jsonify({
                'error': 'Обе книги должны быть в статусе "available"'
            }), 400

        if sender_id == receiver_id:
            return jsonify({
                'error': 'Нельзя обмениваться с самим собой'
            }), 400

        existing = Exchange.query.filter_by(
            sender_id=sender_id,
            receiver_id=receiver_id,
            offered_book_id=offered_book_id,
            requested_book_id=requested_book_id,
            status='pending'
        ).first()
        if existing:
            return jsonify({
                'error': 'Такой обмен уже ожидает подтверждения'
            }), 400

        exchange = Exchange(
            sender_id=sender_id,
            receiver_id=receiver_id,
            offered_book_id=offered_book_id,
            requested_book_id=requested_book_id,
            status='pending',
            created_at=datetime.utcnow()
        )
        db.session.add(exchange)
        db.session.commit()

        return jsonify({
            'message': 'Запрос на обмен отправлен',
            'exchange_id': exchange.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@exchange_bp.route('/<int:exchange_id>', methods=['GET'])
def get_exchange(exchange_id):
    """
    Получить обмен по его ID.
    """
    exchange = Exchange.query.get(exchange_id)
    if not exchange:
        return jsonify({'error': 'Обмен не найден'}), 404

    return jsonify({
        'id': exchange.id,
        'sender_id': exchange.sender_id,
        'receiver_id': exchange.receiver_id,
        'offered_book_id': exchange.offered_book_id,
        'requested_book_id': exchange.requested_book_id,
        'status': exchange.status,
        'created_at': exchange.created_at.isoformat()
    })


@exchange_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_exchanges(user_id):
    """
    Получить все обмены, в которых участвует пользователь (отправленные и
    полученные).
    """
    sent = Exchange.query.filter_by(sender_id=user_id).all()
    received = Exchange.query.filter_by(receiver_id=user_id).all()

    def serialize(ex):
        return {
            'id': ex.id,
            'sender_id': ex.sender_id,
            'receiver_id': ex.receiver_id,
            'offered_book_id': ex.offered_book_id,
            'requested_book_id': ex.requested_book_id,
            'status': ex.status,
            'created_at': ex.created_at.isoformat()
        }

    return jsonify({
        'sent': [serialize(e) for e in sent],
        'received': [serialize(e) for e in received]
    })


@exchange_bp.route('/<int:exchange_id>', methods=['PATCH'])
def update_exchange_status(exchange_id):
    """
    Обновить статус обмена (accepted/declined).
    """
    data = request.get_json() or {}

    exchange = Exchange.query.get(exchange_id)
    if not exchange:
        return jsonify({'error': 'Обмен не найден'}), 404

    if exchange.status in ['accepted', 'declined']:
        return jsonify({'error': 'Этот обмен уже завершён'}), 400

    new_status = data.get('status')
    if new_status not in ['accepted', 'declined']:
        return jsonify({'error': 'Недопустимый статус'}), 400

    offered_book = Book.query.get(exchange.offered_book_id)
    requested_book = Book.query.get(exchange.requested_book_id)
    if not offered_book or not requested_book:
        return jsonify({'error': 'Книги не найдены'}), 404

    exchange.status = new_status
    if new_status == 'accepted':
        offered_book.user_id = exchange.receiver_id
        requested_book.user_id = exchange.sender_id
        offered_book.status = 'unavailable'
        requested_book.status = 'unavailable'
    else:
        offered_book.status = 'available'
        requested_book.status = 'available'

    db.session.commit()
    return jsonify({'message': f'Статус обновлён: {new_status}'}), 200


@exchange_bp.route('/', methods=['GET'])
def list_exchanges():
    """
    Получить список всех обменов.
    """
    exchanges = Exchange.query.all()
    return jsonify([
        {
            'id': ex.id,
            'sender_id': ex.sender_id,
            'receiver_id': ex.receiver_id,
            'offered_book_id': ex.offered_book_id,
            'requested_book_id': ex.requested_book_id,
            'status': ex.status,
            'created_at': ex.created_at.isoformat()
        }
        for ex in exchanges
    ])


@exchange_bp.route('/outgoing', methods=['GET'])
def get_outgoing_requests():
    """
    Получить список исходящих заявок на обмен для пользователя.
    """
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({'error': 'user_id обязателен'}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'user_id должен быть числом'}), 400

    exchanges = Exchange.query.filter_by(sender_id=user_id).all()

    return jsonify([
        {
            'id': ex.id,
            'offered_book_title': ex.offered_book.title,
            'requested_book_title': ex.requested_book.title,
            'to_user': ex.requested_book.owner.username,
            'status': ex.status
        }
        for ex in exchanges
    ]), 200


@exchange_bp.route('/incoming', methods=['GET'])
def get_incoming_requests():
    """
    Получить список входящих заявок на обмен для пользователя.
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({'error': 'user_id обязателен'}), 400

    exchanges = Exchange.query.filter_by(receiver_id=user_id).all()

    return jsonify([
        {
            'id': ex.id,
            'offered_book_title': ex.offered_book.title,
            'requested_book_title': ex.requested_book.title,
            'from_user': ex.sender_user.username,
            'status': ex.status
        }
        for ex in exchanges
    ]), 200
