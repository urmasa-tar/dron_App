document.addEventListener('DOMContentLoaded', function() {
    // Обновление статуса дрона
    const refreshBtn = document.querySelector('.btn-refresh');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.textContent = 'Обновление...';
            setTimeout(() => {
                this.textContent = 'Обновить данные';
                // Здесь будет реальный запрос к API
            }, 1000);
        });
    }
    
    // Обработчики кнопок управления
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.classList.contains('btn-start') ? 'start' : 
                          this.classList.contains('btn-stop') ? 'stop' : 'emergency';
            
            alert(`Команда "${action}" отправлена дрону`);
            // Здесь будет реальный запрос к API
        });
    });
});