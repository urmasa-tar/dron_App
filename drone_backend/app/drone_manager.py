import json
import os
import requests
from datetime import datetime

DRONES_FILE = os.path.join(os.path.dirname(__file__), 'drones.json')

class DroneManager:
    @staticmethod
    def load_drones():
        if not os.path.exists(DRONES_FILE):
            return []
        with open(DRONES_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_drones(drones):
        with open(DRONES_FILE, 'w') as f:
            json.dump(drones, f, indent=2)

    @staticmethod
    def check_drone_connection(ip):
        try:
            response = requests.get(f"http://{ip}:8080/ping", timeout=3)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def add_drone(name, ip):
        drones = DroneManager.load_drones()
        new_id = max(drone['id'] for drone in drones) + 1 if drones else 1
        
        new_drone = {
            'id': new_id,
            'name': name,
            'ip': ip,
            'status': 'offline',
            'battery': 0,
            'last_seen': None,
            'is_connected': False
        }
        
        drones.append(new_drone)
        DroneManager.save_drones(drones)
        return new_drone

    @staticmethod
    def update_drone_status(drone_id):
        drones = DroneManager.load_drones()
        drone = next((d for d in drones if d['id'] == drone_id), None)
        
        if drone:
            try:
                response = requests.get(f"http://{drone['ip']}:8080/status", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    drone['status'] = data.get('status', 'offline')
                    drone['battery'] = data.get('battery', 0)
                    drone['last_seen'] = datetime.now().isoformat()
                    drone['is_connected'] = True
                else:
                    drone['is_connected'] = False
            except:
                drone['is_connected'] = False
            
            DroneManager.save_drones(drones)
            return drone
        return None