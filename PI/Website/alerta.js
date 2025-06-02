document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const nombre = document.getElementById('nombre');
    const apellidos = document.getElementById('apellidos');
    const email = document.getElementById('email');
    const sintomas = document.getElementById('sintomas');
    const accionar = document.getElementById('accionar');

    function verificarCampos() {
        if (nombre.value.trim() && apellidos.value.trim() && email.value.trim() && sintomas.value.trim()) {
            accionar.disabled = false;
        } else {
            accionar.disabled = true;
        }
    }

    nombre.addEventListener('input', verificarCampos);
    apellidos.addEventListener('input', verificarCampos);
    email.addEventListener('input', verificarCampos);
    sintomas.addEventListener('input', verificarCampos);

    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        if (nombre.value.trim() && apellidos.value.trim() && email.value.trim() && sintomas.value.trim()) {
            alert("Se ha contactado al especialista. \nEspera a que se contacte contigo. Puedes contactar con sus redes sociales, email o número.");
            form.reset();
            accionar.disabled = true;
        } else {
            alert("Por favor, llena todos los campos.");
        }
    });
});
