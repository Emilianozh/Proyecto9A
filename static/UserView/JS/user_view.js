
// Inicialmente ocultar el widget completo y mostrar solo el botón flotante
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ia-chat-widget').style.display = 'none';
    document.getElementById('ia-chat-toggle-btn').style.display = 'flex';

    // Oculta el badge "Nuevo" después de 5 minutos (300000 ms)
    document.querySelectorAll('[id^="badge-nuevo-"]').forEach(function(badge) {
        setTimeout(function() {
            badge.style.display = 'none';
        }, 300000); // 5 minutos
    });
});

function mostrarIAChat() {
    document.getElementById('ia-chat-widget').style.display = 'block';
    document.getElementById('ia-chat-toggle-btn').style.display = 'none';
}
function toggleIAChat() {
    document.getElementById('ia-chat-widget').style.display = 'none';
    document.getElementById('ia-chat-toggle-btn').style.display = 'flex';
}
