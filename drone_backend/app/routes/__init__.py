from flask import Blueprint

# Создаем основной Blueprint
bp = Blueprint('website', __name__)

# Импортируем роуты после создания bp, чтобы избежать circular imports
from app.routes import website