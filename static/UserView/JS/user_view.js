// No JS necesario actualmente para user_view, solo estructura para futuro uso.

document.addEventListener('DOMContentLoaded', function() {
    // Oculta el badge "Nuevo" después de 5 minutos (300000 ms)
    document.querySelectorAll('[id^="badge-nuevo-"]').forEach(function(badge) {
        setTimeout(function() {
            badge.style.display = 'none';
        }, 300000); // 5 minutos
    });
});
