# BookExchange — сервис для обмена книгами

## Описание

BookExchange — это платформа, где пользователи могут обмениваться книгами, искать интересные издания по фильтрам, предлагать свои книги и отслеживать историю обменов. Проект реализован на Flask (backend) и React (frontend), использует PostgreSQL и полностью контейнеризирован с помощью Docker.

---

## Структура проекта

```
.
├── app/                    # Backend (Flask)
│   ├── __init__.py         # Инициализация приложения
│   ├── extensions.py       # Расширения (SQLAlchemy)
│   ├── models.py           # Модели БД: User, Book, Exchange
│   ├── routes/             # Маршруты API (users, books, exchange)
│   ├── static/swagger.yaml # Swagger-документация API
├── book-exchange-frontend/ # Frontend (React)
│   ├── public/             # Статические файлы и изображения
│   └── src/                # Исходный код React-приложения
├── tests/                  # Unit-тесты backend
├── Dockerfile              # Dockerfile для backend
├── docker-compose.yml      # Docker Compose для backend и БД
├── requirements.txt        # Python-зависимости
├── create_db.py            # Скрипт инициализации БД и создания администратора
├── run.py                  # Точка входа Flask-приложения
└── README.md               # Описание проекта
```

---

## Как запустить проект

### 1. Клонируйте репозиторий

### 2. Запуск через Docker Compose

```bash
docker-compose up --build
```

### 3. Отдельно необходимо запустить Flask

```bash
flask run
```
- Backend будет доступен на [http://localhost:5001](http://localhost:5001)
- Swagger UI: [http://localhost:5001/swagger](http://localhost:5001/swagger)
- База данных PostgreSQL: порт 5432

### 4. Запуск фронтенда (React)

Перейдите в папку `book-exchange-frontend` и выполните:
```bash
npm install
npm run dev
```
- Фронтенд будет доступен на [http://localhost:5173](http://localhost:5173) (или другой порт, указанный в консоли)

### 5. Инициализация базы данных и создание администратора

```bash
python create_db.py
```
- Скрипт удалит старую и создаст новую базу данных (если она была)
- Администратор создается автоматически (логин: admin, пароль: admin123)
- Если администратор уже есть, скрипт просто выведет сообщение

---

## Swagger-документация

- Открыть [http://localhost:5001/swagger](http://localhost:5001/swagger)
- Вся структура и примеры запросов доступны в `app/static/swagger.yaml`

---

## Тестирование

- Все основные функции покрыты unit-тестами (папка `tests/`)
- Запуск тестов:
  ```bash
  python -m unittest discover tests
  ```

---

## Проверка кода

- Код проверен на соответствие стандарту PEP 8 с помощью flake8
- Максимальная длина строки: 79 символов
- Запуск проверки:
  ```bash
  flake8 app/ tests/
  ```

---

## Рекомендации

- Для полноценной работы убедитесь, что все сервисы подняты через Docker Compose.
- Swagger UI позволяет тестировать API прямо из браузера.
- Для CI рекомендуется добавить GitHub Actions или аналогичный pipeline для автозапуска тестов.