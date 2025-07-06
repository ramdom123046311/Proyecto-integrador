document.getElementById('registroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    
    // Validación de contraseñas coincidentes
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        return;
    }

    // Validación de longitud mínima
    if (password.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres');
        return;
    }

    // Mostrar indicador de carga
    const submitBtn = document.getElementById('registro');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registrando...';

    // Enviar datos al servidor
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json().then(data => {
                if (data.errors) {
                    // Mostrar errores del servidor
                    Object.keys(data.errors).forEach(field => {
                        const input = document.querySelector(`[name="${field}"]`);
                        const errorDiv = input.nextElementSibling;
                        
                        if (input && errorDiv && errorDiv.classList.contains('campo-error')) {
                            input.classList.add('input-error');
                            errorDiv.textContent = data.errors[field];
                            errorDiv.style.display = 'flex';
                        }
                    });
                } else if (data.message) {
                    alert(data.message);
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error en el registro. Por favor intenta nuevamente.');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-user-plus"></i> Regístrate';
    });
});