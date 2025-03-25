from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Создаем папку для launch-файлов
    import os
    os.makedirs('launch_files', exist_ok=True)
    
    from app.routes.website import bp as website_bp
    app.register_blueprint(website_bp)
    
    return app