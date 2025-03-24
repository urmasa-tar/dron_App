from flask import Blueprint, render_template
from app.data import drones, tasks

bp = Blueprint('website', __name__)

@bp.route('/')
def index():
    return render_template('index.html', drones=drones, tasks=tasks)

@bp.route('/drones')
def drones_list():
    return render_template('drones.html', drones=drones)

@bp.route('/tasks')
def tasks_list():
    return render_template('tasks.html', tasks=tasks)