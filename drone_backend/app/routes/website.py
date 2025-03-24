from flask import render_template
from app.data import drones, tasks
from app.routes import bp  # Импортируем bp из родительского модуля

@bp.route('/')
def index():
    return render_template('index.html', drones=drones, tasks=tasks)

@bp.route('/drones')
def drones_list():
    return render_template('drones.html', drones=drones)

@bp.route('/drone/<int:drone_id>')
def drone_detail(drone_id):
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        return "Drone not found", 404
    return render_template('drone_detail.html', drone=drone)