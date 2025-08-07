// Funciones para el chat IA
function toggleIAChat() {
    var body = document.getElementById('ia-chat-body');
    var icon = document.getElementById('ia-toggle-icon');
    if (body.style.display === 'none') {
        body.style.display = 'block';
        icon.innerHTML = '&#9650;';
    } else {
        body.style.display = 'none';
        icon.innerHTML = '&#9660;';
    }
}

function enviarMensajeIA() {
    var input = document.getElementById('user-input').value;
    document.getElementById('loading-ia').style.display = 'block';
    document.getElementById('ia-response').style.display = 'none';
    fetch('/gemini_chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: input})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('ia-response').innerText = data.response;
        document.getElementById('ia-response').style.display = 'block';
        document.getElementById('loading-ia').style.display = 'none';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('ia-chat-body')) {
        document.getElementById('ia-chat-body').style.display = 'block';
    }
});
