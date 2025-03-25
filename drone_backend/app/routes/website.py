from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify, abort
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
    """Главная страница со списком всех дронов"""
    return render_template('index.html', drones=drones)

@bp.route('/add_drone', methods=['GET', 'POST'])
def add_drone():
    """Добавление нового дрона"""
    if request.method == 'POST':
        # Валидация данных
        name = request.form.get('name', '').strip()
        ip_address = request.form.get('ip_address', '').strip()
        
        if not name or not ip_address:
            abort(400, description="Необходимо указать имя и IP-адрес дрона")
            
        # Проверка уникальности IP
        if any(d['ip_address'] == ip_address for d in drones):
            abort(400, description="Дрон с таким IP-адресом уже существует")
            
        # Создание записи о дроне
        drone_data = {
            'id': len(drones) + 1,
            'name': name,
            'ip_address': ip_address,
            'node_name': f"mavros_{len(drones) + 1}",
            'system_id': len(drones) + 1,
            'status': 'disconnected',
            'added_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'process_id': None
        }
        
        # Генерация launch-файла
        try:
            generate_launch_file(drone_data)
            drones.append(drone_data)
            return redirect(url_for('website.index'))
        except Exception as e:
            abort(500, description=f"Ошибка при создании конфигурации: {str(e)}")
    
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
    """Подключение к дрону через MAVROS"""
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    # Проверяем, не подключен ли уже дрон
    if drone['status'] == 'connected':
        return jsonify({
            "status": "error",
            "message": "Дрон уже подключен"
        }), 400
    
    launch_file = f"launch_files/{drone['name']}.launch"
    if not os.path.exists(launch_file):
        generate_launch_file(drone)
    
    try:
        # Запускаем launch-файл
        process = subprocess.Popen(
            ["roslaunch", launch_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Даем время на инициализацию
        try:
            process.wait(timeout=2)
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, "roslaunch")
        except subprocess.TimeoutExpired:
            # Процесс работает в фоне - это нормально
            pass
            
        drone['status'] = 'connected'
        drone['process_id'] = process.pid
        
        return jsonify({
            "status": "success",
            "message": f"Дрон {drone['name']} ({drone['ip_address']}) подключен",
            "pid": process.pid
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка запуска: {e.stderr}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/drone/<int:drone_id>/disconnect', methods=['POST'])
def disconnect_drone(drone_id):
    """Отключение дрона"""
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
    if drone['status'] != 'connected' or not drone.get('process_id'):
        return jsonify({
            "status": "error",
            "message": "Дрон не был подключен"
        }), 400
    
    try:
        # Завершаем процесс
        os.kill(drone['process_id'], 9)
        drone['status'] = 'disconnected'
        drone['process_id'] = None
        
        return jsonify({
            "status": "success",
            "message": f"Дрон {drone['name']} отключен"
        })
    except ProcessLookupError:
        # Процесс уже завершен
        drone['status'] = 'disconnected'
        drone['process_id'] = None
        return jsonify({
            "status": "success",
            "message": "Соединение уже было разорвано"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/download/launch/<drone_name>')
def download_launch(drone_name):
    """Скачивание launch-файла"""
    drone = next((d for d in drones if d['name'] == drone_name), None)
    if not drone:
        abort(404, description="Дрон не найден")
    
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

@bp.route('/api/drones')
def api_drones():
    """API endpoint для получения списка дронов"""
    return jsonify([{
        'id': d['id'],
        'name': d['name'],
        'ip_address': d['ip_address'],
        'status': d['status']
    } for d in drones])