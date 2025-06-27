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
    // Save changes (for now, just close modal)
    document.getElementById('saveEdit').onclick = function() {
        // Aquí puedes agregar lógica para guardar los cambios
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
