from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Регистрируем Blueprint
    from app.routes import bp as website_bp
    app.register_blueprint(website_bp)
    
    return app