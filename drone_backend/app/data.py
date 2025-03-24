from datetime import datetime

drones = [
    {
        'id': 1,
        'name': 'Clover-001',
        'status': 'idle',
        'ip_address': '192.168.1.100',
        'last_seen': datetime.now(),
        'battery': 95,
        'signal': 'strong'
    },
    {
        'id': 2,
        'name': 'Clover-002',
        'status': 'busy',
        'ip_address': '192.168.1.101',
        'last_seen': datetime.now(),
        'battery': 78,
        'signal': 'medium'
    }
]

tasks = [
    {
        'id': 1,
        'drone_id': 2,
        'task_name': 'Инспекция территории',
        'status': 'in_progress',
        'created_at': datetime.now()
    }
]

def get_next_id(collection):
    if not collection:
        return 1
    return max(item['id'] for item in collection) + 1