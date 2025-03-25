import subprocess
import platform

class DroneManager:
    @staticmethod
    def check_connection(ip):
        """Проверяет, доступен ли дрон (через ping или ROS-команды)."""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", ip]
            response = subprocess.run(command, stdout=subprocess.PIPE, timeout=2)
            return response.returncode == 0
        except:
            return False