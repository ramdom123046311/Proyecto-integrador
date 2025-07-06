document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            
            // Mostrar estado de carga
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando sesión...';
            
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
                        if (data.error) {
                            // Mostrar mensaje de error
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'alert alert-error';
                            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${data.error}`;
                            
                            const header = document.querySelector('.login-header');
                            if (header) {
                                const existingAlert = header.querySelector('.alert-error');
                                if (existingAlert) {
                                    header.removeChild(existingAlert);
                                }
                                header.appendChild(errorDiv);
                            }
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al iniciar sesión. Por favor intenta nuevamente.');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Iniciar sesión';
            });
        });
    }
});