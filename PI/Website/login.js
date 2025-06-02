// Función que valida el inicio de sesión
function validarLogin() {
    // Obtener los valores ingresados en los campos
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Obtener los usuarios desde localStorage
    const usuarios = JSON.parse(localStorage.getItem("usuarios")) || {};

    // Verificar si el usuario existe en localStorage
    if (usuarios[email] && usuarios[email].password === password) {
        // Si existe, redirigir al usuario a la página de inicio o al perfil
        alert("Inicio de sesión exitoso");
        window.location.href = "index.html"; // Redirige a la página principal después del login
        return false; // Evita que el formulario se envíe
    } else {
        // Si no existe o la contraseña es incorrecta, mostrar un mensaje de error
        alert("Correo electrónico o contraseña incorrectos");
        return false; // Evita que el formulario se envíe
    }
}
