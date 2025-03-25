from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from drone_manager import DroneManager

app = Flask(__name__)

# Путь к файлу с данными о дронах
DRONES_FILE = "drones.json"

def load_drones():
    """Загружает данные о дронах из JSON-файла с обработкой ошибок."""
    if not os.path.exists(DRONES_FILE):
        return []  # Файла нет — возвращаем пустой список
    
    try:
        with open(DRONES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []  # Файл повреждён — возвращаем пустой список

def save_drones(drones):
    """Сохраняет данные о дронах в JSON-файл."""
    with open(DRONES_FILE, "w") as f:
        json.dump(drones, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    drones = load_drones()
    # Обновляем статус каждого дрона
    for drone in drones:
        drone["is_online"] = DroneManager.check_connection(drone["ip"])
    return render_template("index.html", drones=drones)

@app.route("/drone/<int:drone_id>")
def drone_page(drone_id):
    drones = load_drones()
    drone = next((d for d in drones if d["id"] == drone_id), None)
    if not drone:
        return "Дрон не найден", 404
    drone["is_online"] = DroneManager.check_connection(drone["ip"])
    return render_template("drone.html", drone=drone)

@app.route("/add_drone", methods=["GET", "POST"])
def add_drone():
    if request.method == "POST":
        name = request.form.get("name").strip()
        ip = request.form.get("ip").strip()
        if not name or not ip:
            return "Не указаны имя или IP", 400
        
        drones = load_drones()
        new_drone = {
            "id": len(drones) + 1,
            "name": name,
            "ip": ip,
            "is_online": False  # Статус обновится при следующей проверке
        }
        drones.append(new_drone)
        save_drones(drones)
        return redirect(url_for("index"))
    
    return render_template("add_drone.html")

@app.route("/api/drone_status/<int:drone_id>")
def drone_status(drone_id):
    drones = load_drones()
    drone = next((d for d in drones if d["id"] == drone_id), None)
    if not drone:
        return jsonify({"error": "Дрон не найден"}), 404
    
    is_online = DroneManager.check_connection(drone["ip"])
    return jsonify({"is_online": is_online})

if __name__ == "__main__":
    # Создаём файл drones.json, если его нет
    if not os.path.exists(DRONES_FILE):
        with open(DRONES_FILE, "w") as f:
            f.write("[]")
    app.run(debug=True)