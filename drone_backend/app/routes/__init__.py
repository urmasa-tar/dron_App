from flask import Blueprint

# Создаем основной Blueprint для веб-роутов
bp = Blueprint('website', __name__)

# Импортируем все роуты после создания bp, чтобы избежать circular imports
from app.routes import website