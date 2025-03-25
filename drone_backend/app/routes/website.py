from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, abort
from datetime import datetime
import os
import subprocess
from pathlib import Path
from app.utils.launch_generator import generate_launch_file

bp = Blueprint('website', __name__)

# Временное хранилище дронов (в реальном проекте следует использовать БД)
drones = []

@bp.route('/')
def index():
    """Главная страница со списком дронов"""
    return render_template('index.html', drones=drones)

@bp.route('/add_drone', methods=['GET', 'POST'])
def add_drone():
    """Страница добавления нового дрона"""
    if request.method == 'POST':
        # Валидация данных
        if not request.form.get('name') or not request.form.get('fcu_url'):
            abort(400, description="Необходимо указать имя дрона и FCU URL")
        
        drone_data = {
            'id': len(drones) + 1,
            'name': request.form['name'],
            'fcu_url': request.form['fcu_url'],
            'node_name': f"mavros_{len(drones) + 1}",
            'system_id': len(drones) + 1,
            'status': 'disconnected',
            'added_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        drones.append(drone_data)
        generate_launch_file(drone_data)
        return redirect(url_for('website.index'))
    
    return render_template('add_drone.html')

@bp.route('/drone/<int:drone_id>')
def drone_detail(drone_id):
    """Страница управления конкретным дроном"""
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404, description="Дрон не найден")
    return render_template('drone_detail.html', drone=drone)

@bp.route('/drone/<int:drone_id>/connect', methods=['POST'])
def connect_drone(drone_id):
    """API endpoint для подключения к дрону"""
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    try:
        # Запускаем launch-файл в отдельном процессе
        launch_file = f"launch_files/{drone['name']}.launch"
        process = subprocess.Popen(
            ["roslaunch", launch_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Обновляем статус дрона
        drone['status'] = 'connected'
        drone['process_id'] = process.pid
        
        return {
            "status": "success",
            "message": f"Дрон {drone['name']} подключен",
            "pid": process.pid,
            "fcu_url": drone['fcu_url']
        }, 200
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

@bp.route('/download/launch/<drone_name>')
def download_launch(drone_name):
    """Скачивание launch-файла"""
    drone = next((d for d in drones if d['name'] == drone_name), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    # Проверяем существование файла
    launch_path = Path('launch_files') / f"{drone_name}.launch"
    if not launch_path.exists():
        generate_launch_file(drone)
    
    return send_from_directory(
        'launch_files',
        f"{drone_name}.launch",
        as_attachment=True,
        mimetype='application/xml',
        download_name=f"{drone_name}_mavros.launch"
    )

@bp.route('/drone/<int:drone_id>/disconnect', methods=['POST'])
def disconnect_drone(drone_id):
    """Отключение дрона"""
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    if 'process_id' not in drone:
        return {"status": "error", "message": "Дрон не был подключен"}, 400
    
    try:
        # Завершаем процесс roslaunch
        os.kill(drone['process_id'], 9)
        drone['status'] = 'disconnected'
        del drone['process_id']
        
        return {
            "status": "success",
            "message": f"Дрон {drone['name']} отключен"
        }, 200
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500