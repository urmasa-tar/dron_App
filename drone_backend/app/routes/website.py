from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, abort
from pathlib import Path
import os
from datetime import datetime
from app.utils.launch_generator import generate_launch_file

bp = Blueprint('website', __name__)

# Временное хранилище дронов (в реальном проекте замените на БД)
drones = []

@bp.route('/')
def index():
    return render_template('index.html', drones=drones)

@bp.route('/add_drone', methods=['GET', 'POST'])
def add_drone():
    if request.method == 'POST':
        drone_data = {
            'id': len(drones) + 1,
            'name': request.form['name'],
            'ip': request.form['ip'],
            'port': request.form.get('port', '14550'),
            'ros_port': request.form.get('ros_port', '11311'),
            'status': 'disconnected',
            'added_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        drones.append(drone_data)
        
        # Генерируем launch-файл
        os.makedirs('launch_files', exist_ok=True)
        generate_launch_file(drone_data)
        
        return redirect(url_for('website.index'))
    return render_template('add_drone.html')

@bp.route('/drone/<int:drone_id>')
def drone_detail(drone_id):
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404)
    return render_template('drone_detail.html', drone=drone)

@bp.route('/download/launch/<drone_name>')
def download_launch(drone_name):
    # Проверяем существование дрона
    drone = next((d for d in drones if d['name'] == drone_name), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    # Путь к файлам
    launch_dir = Path('launch_files')
    filename = f"{drone_name}.launch"
    filepath = launch_dir / filename
    
    # Если файла нет - создаем
    if not filepath.exists():
        generate_launch_file(drone)
    
    # Отправляем файл
    return send_from_directory(
        launch_dir.resolve(),
        filename,
        as_attachment=True,
        mimetype='application/xml',
        download_name=f"{drone_name}_mavros.launch"
    )