document.getElementById('registroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById('nombre').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    // Validaciones
    if (password !== confirm_password) {
        alert('Las contraseñas no coinciden');
        return;
    }

    if (password.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres');
        return;
    }

    // Enviar datos al servidor
    fetch("{{ url_for('procesar_registro') }}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nombre: nombre,
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registro exitoso');
            window.location.href = "{{ url_for('perfil') }}";
        } else {
            alert(data.message || 'Error en el registro');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error en el registro');
    });
});