function eliminarDelCarrito(idArticulo) {
    fetch('/eliminar_carrito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_articulo: idArticulo })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            location.reload();
        } else {
            alert('Error al eliminar del carrito');
        }
    });
}
