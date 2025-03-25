from flask import Flask
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'
    
    # Регистрируем Blueprint
    from app.routes import bp
    app.register_blueprint(bp)
    
    # Добавляем фильтр для дат
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%d.%m.%Y %H:%M'):
        if value is None:
            return ""
        if isinstance(value, str):
            return datetime.fromisoformat(value).strftime(format)
        return value.strftime(format)
    
    return app