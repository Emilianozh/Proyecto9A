// Modal functionality for Edit buttons

document.addEventListener('DOMContentLoaded', function() {
    // Open modal on edit button click
    document.querySelectorAll('.icon-btn.edit').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const row = btn.closest('tr');
            const id = row.children[0].textContent;
            const nombre = row.children[1].textContent;
            const cantidad = row.children[2].textContent;
            const precio = row.children[3].textContent.replace('$','');
            document.getElementById('modal-id').value = id;
            document.getElementById('modal-nombre').value = nombre;
            document.getElementById('modal-cantidad').value = cantidad;
            document.getElementById('modal-precio').value = precio;
            document.getElementById('editModal').style.display = 'block';
        });
    });
    // Close modal
    document.getElementById('closeModal').onclick = function() {
        document.getElementById('editModal').style.display = 'none';
    };
    // Save changes (envía los datos por AJAX a /editar)
    document.getElementById('saveEdit').onclick = function() {
        const id = document.getElementById('modal-id').value;
        const nombre = document.getElementById('modal-nombre').value;
        const stock = document.getElementById('modal-cantidad').value;
        const precio = document.getElementById('modal-precio').value;

        fetch('/editar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_articulo: id, nombre, stock, precio })
        })
        .then(response => {
            if (response.ok) {
                location.reload(); // Recarga la página para ver los cambios
            } else {
                alert('Error al actualizar');
            }
        });

        document.getElementById('editModal').style.display = 'none';
    };
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('editModal');
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
});
