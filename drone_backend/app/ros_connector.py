import roslibpy
from threading import Thread

class ROSConnector:
    def __init__(self):
        self.client = roslibpy.Ros(host='raspberrypi.local', port=9090)
        self.connected = False
        
    def connect(self):
        def run():
            try:
                self.client.run()
                self.connected = True
            except Exception as e:
                print(f"ROS connection error: {e}")
                
        Thread(target=run).start()
        
    def call_service(self, service_name, service_type, request_data):
        if not self.connected:
            self.connect()
            
        service = roslibpy.Service(self.client, service_name, service_type)
        request = roslibpy.ServiceRequest(request_data)
        return service.call(request)