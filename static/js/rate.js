document.addEventListener('DOMContentLoaded', function() {
    // Анимация прогресс-баров
    const ratingBars = document.querySelectorAll('.rating-bar');
    ratingBars.forEach(bar => {
        // Сохраняем оригинальную ширину
        const originalWidth = bar.style.width;
        // Сбрасываем ширину для анимации
        bar.style.width = '0';
        
        // Запускаем анимацию после небольшой задержки
        setTimeout(() => {
            bar.style.width = originalWidth;
        }, 300);
    });
    
    // Плавное появление контейнера
    const container = document.querySelector('.rating-container');
    container.style.opacity = '0';
    container.style.transform = 'translateY(20px)';
    container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    
    setTimeout(() => {
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 100);
    
    // Анимация при наведении на строки
    const tableRows = document.querySelectorAll('.rating-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.zIndex = '10';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.zIndex = '1';
        });
    });
});