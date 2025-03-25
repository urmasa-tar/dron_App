from flask import Blueprint

# Создаем основной Blueprint
bp = Blueprint('main', __name__)

# Импортируем роуты после создания bp
from app.routes import website, api