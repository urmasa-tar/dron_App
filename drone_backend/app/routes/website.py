from flask import render_template, request, redirect, url_for, flash
from app.drone_manager import DroneManager
from app.routes import bp  # Импортируем bp из __init__.py

@bp.route('/')
def index():
    drones = DroneManager.load_drones()
    return render_template('index.html', drones=drones)

@bp.route('/add_drone', methods=['GET', 'POST'])
def add_drone():
    if request.method == 'POST':
        name = request.form.get('name')
        ip = request.form.get('ip')
        
        if not name or not ip:
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('main.add_drone'))
        
        if not DroneManager.check_drone_connection(ip):
            flash('Не удалось подключиться к дрону по указанному IP', 'error')
            return redirect(url_for('main.add_drone'))
        
        DroneManager.add_drone(name, ip)
        flash('Дрон успешно добавлен', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_drone.html')

@bp.route('/drone/<int:drone_id>')
def drone_detail(drone_id):
    drone = DroneManager.update_drone_status(drone_id)
    if not drone:
        flash('Дрон не найден', 'error')
        return redirect(url_for('main.index'))
    return render_template('drone_detail.html', drone=drone)