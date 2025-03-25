from flask import jsonify
from app.drone_manager import DroneManager
from app.routes import bp  # Импортируем bp из __init__.py

@bp.route('/api/drone/<int:drone_id>/<command>', methods=['POST'])
def send_command(drone_id, command):
    drone = DroneManager.update_drone_status(drone_id)
    if not drone:
        return jsonify({'error': 'Drone not found'}), 404
    
    try:
        # Здесь будет реальная команда к Gazebo API
        return jsonify({
            'success': True,
            'message': f'Command {command} sent to drone {drone_id}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500