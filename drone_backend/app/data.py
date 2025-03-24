from datetime import datetime

drones = [
    {
        'id': 1,
        'name': 'Demo Drone 1',
        'ip': 'localhost',
        'status': 'idle',
        'battery': 87,
        'last_seen': datetime.now()
    }
]

def get_next_id(collection):
    return max(d['id'] for d in collection) + 1 if collection else 1

def add_new_drone(drone_data):
    drones.append(drone_data)