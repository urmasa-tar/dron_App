from flask import Blueprint, jsonify, request
from app.data import drones, tasks, get_next_id
from datetime import datetime

# Создаем Blueprint с именем 'api'
bp = Blueprint('api', __name__)

@bp.route('/drones', methods=['GET'])
def get_drones():
    return jsonify(drones)

@bp.route('/drones', methods=['POST'])
def register_drone():
    data = request.get_json()
    new_drone = {
        'id': get_next_id(drones),
        'name': data['name'],
        'status': 'idle',
        'ip_address': data['ip_address'],
        'last_seen': datetime.now()
    }
    drones.append(new_drone)
    return jsonify(new_drone), 201

@bp.route('/drones/<int:drone_id>', methods=['GET'])
def get_drone(drone_id):
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if drone:
        return jsonify(drone)
    return jsonify({'error': 'Drone not found'}), 404

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        'id': get_next_id(tasks),
        'drone_id': data['drone_id'],
        'task_name': data['task_name'],
        'coordinates': data['coordinates'],
        'status': 'pending',
        'created_at': datetime.now()
    }
    tasks.append(new_task)
    return jsonify(new_task), 201