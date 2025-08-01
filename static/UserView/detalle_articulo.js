function agregarAlCarrito(idArticulo) {
    var cantidad = document.getElementById('cantidad').value;
    fetch('/agregar_carrito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_articulo: idArticulo, cantidad: cantidad })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert('Artículo agregado al carrito');
        } else {
            alert('Error al agregar al carrito');
        }
    });
}

let currentRating = 0;
function setRating(rating) {
    currentRating = parseInt(rating); // Asegura que sea número
    document.getElementById('rating').value = currentRating;
    for(let i=1; i<=5; i++) {
        document.getElementById('star'+i).className = i <= currentRating ? 'bi bi-star-fill text-warning' : 'bi bi-star';
    }
}
function enviarRating(e) {
    e.preventDefault();
    fetch('/calificar_articulo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_articulo: document.getElementById('ratingForm').dataset.articuloId, estrellas: currentRating })
    })
    .then(r => r.json())
    .then(data => {
        if(data.success) {
            alert('¡Gracias por tu calificación!');
            location.reload();
        } else {
            alert('Error al enviar calificación');
        }
    });
}
