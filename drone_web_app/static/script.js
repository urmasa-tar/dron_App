async function pingDrone(droneId) {
    const response = await fetch(`/api/drone_status/${droneId}`);
    const data = await response.json();
    
    const statusElement = document.querySelector(`.status-${data.is_online ? 'online' : 'offline'}`);
    const messageElement = document.getElementById("status-message");
    
    if (data.is_online) {
        messageElement.textContent = "Дрон доступен!";
    } else {
        messageElement.textContent = "Дрон недоступен.";
    }
}

// Автоматическое обновление статуса каждые 5 секунд
setInterval(() => {
    document.querySelectorAll(".drone-list li").forEach(item => {
        const droneId = item.getAttribute("data-drone-id");
        if (droneId) pingDrone(droneId);
    });
}, 5000);

document.querySelectorAll(".ping-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const droneId = btn.getAttribute("data-drone-id");
        pingDrone(droneId);
    });
});