"""
Создание и инициализация базы данных, создание администратора.
"""
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("База данных создана")

    existing_admin = User.query.filter_by(username='admin').first()
    if not existing_admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Администратор создан: admin / admin123")
    else:
        print("Администратор уже существует")
