import subprocess
from flask import jsonify

@bp.route('/api/drone/<int:drone_id>/connect', methods=['POST'])
def connect_drone(drone_id):
    drone = next((d for d in drones if d['id'] == drone_id), None)
    if not drone:
        return jsonify({"error": "Drone not found"}), 404
    
    try:
        # Запускаем ROS launch файл
        launch_file = f"launch_files/{drone['name']}.launch"
        process = subprocess.Popen(
            ["roslaunch", launch_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Обновляем статус дрона
        drone['status'] = 'connected'
        drone['ros_pid'] = process.pid
        
        return jsonify({
            "success": True,
            "message": f"Launch file executed for {drone['name']}",
            "pid": process.pid
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500