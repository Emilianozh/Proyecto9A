// Validación frontend para el formulario de registro

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form[action="/registro"]');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    let valid = true;
    let mensajes = [];
    const nombre = form.elements['nombre'].value.trim();
    const apellido = form.elements['apellido'].value.trim();
    const correo = form.elements['correo'].value.trim();
    const password = form.elements['password'].value;
    const telefono = form.elements['telefono'].value.trim();
    // Validación nombre y apellido
    if (!nombre || !apellido) {
      valid = false;
      mensajes.push('Nombre y apellido son obligatorios.');
    }
    // Validación correo
    const correoRegex = /^[^@]+@[^@]+\.[^@]+$/;
    if (!correoRegex.test(correo)) {
      valid = false;
      mensajes.push('Correo electrónico no válido.');
    }
    // Validación contraseña
    if (password.length < 6) {
      valid = false;
      mensajes.push('La contraseña debe tener al menos 6 caracteres.');
    }
    // Validación teléfono (opcional)
    if (telefono && !/^\+?\d{7,15}$/.test(telefono)) {
      valid = false;
      mensajes.push('Teléfono no válido.');
    }
    // Mostrar mensajes
    let errorDiv = document.getElementById('registroError');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.id = 'registroError';
      errorDiv.className = 'alert alert-danger';
      form.prepend(errorDiv);
    }
    if (!valid) {
      e.preventDefault();
      errorDiv.innerHTML = mensajes.join('<br>');
      errorDiv.style.display = 'block';
    } else {
      errorDiv.style.display = 'none';
    }
  });
});
