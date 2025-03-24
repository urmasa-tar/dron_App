document.addEventListener('DOMContentLoaded', function() {
    // Обработчики кнопок
    document.querySelector('.start-btn').addEventListener('click', function() {
        alert('Команда "Start" отправлена дрону');
        // Здесь будет AJAX запрос к API
    });
    
    document.querySelector('.killswitch-btn').addEventListener('click', function() {
        if(confirm('Вы уверены, что хотите активировать Kill Switch?')) {
            alert('Kill Switch активирован');
            // Здесь будет AJAX запрос к API
        }
    });
    
    document.querySelector('.land-btn').addEventListener('click', function() {
        alert('Команда "Land" отправлена дрону');
        // Здесь будет AJAX запрос к API
    });
});