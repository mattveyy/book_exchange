"""
Запуск Flask-приложения и Swagger UI.
"""
from flask_swagger_ui import get_swaggerui_blueprint
from app import create_app

app = create_app()

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Book Exchange API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
