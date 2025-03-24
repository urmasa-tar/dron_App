from flask import render_template, request, redirect, url_for
from app.data import drones, add_new_drone, get_next_id
from app.routes import bp  # Импортируем bp из родительского модуля

@bp.route('/')
def index():
    return render_template('index.html', drones=drones)

@bp.route('/add_drone', methods=['GET', 'POST'])
def add_drone():
    if request.method == 'POST':
        drone_id = get_next_id(drones)
        new_drone = {
            'id': drone_id,
            'name': request.form['name'],
            'ip': request.form.get('ip', 'localhost'),
            'status': 'offline',
            'battery': 0,
            'last_seen': None
        }
        add_new_drone(new_drone)
        return redirect(url_for('website.index'))
    return render_template('add_drone.html')

@bp.route('/drone/<int:drone_id>')
def drone_detail(drone_id):
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        return "Drone not found", 404
    return render_template('drone_detail.html', drone=drone)