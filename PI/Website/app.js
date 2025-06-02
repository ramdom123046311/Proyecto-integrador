// Diccionario de citas
let citas = {};


citas["CITA-M3UUFL3R"] = {
  nombre: "Zoe",
  paterno: "Huerta",
  materno: "Frias",
  especialista: "Dr. Rodrigo Betancourt - Ginecología y Obstetricia",
  fecha: "28-12-2024",
  hora: "11:20"
};

citas["CITA-M3UXLMV3"] = {
  nombre: "Naomi",
  paterno: "Carrillo",
  materno: "Gonzalez",
  especialista: "Dra. Ana López - Pediatría",
  fecha: "29-12-2024",
  hora: "12:20"
};


let citasEnLinea = {}; 
let citasPresenciales = {}; 

// Función para guardar una nueva cita
function guardarCita() {
    const nombre = document.getElementById("nombre").value.trim();
    const paterno = document.getElementById("paterno").value.trim();
    const materno = document.getElementById("materno").value.trim();
    const especialista = document.getElementById("especialista").value.trim();
    const modalidad = document.getElementById("modalidad").value.trim();
    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora").value;
  
    // Validar campos obligatorios
    if (!nombre || !paterno || !materno || !especialista || !fecha || !hora || !modalidad) {
      alert("Por favor, completa todos los campos obligatorios.");
      return;
    }
  
    // Validar fecha y hora
    const fechaSeleccionada = new Date(`${fecha}T${hora}:00`);
    const ahora = new Date();
  
    if (isNaN(fechaSeleccionada)) {
      alert("La fecha o la hora seleccionadas no son válidas.");
      return;
    }
  
    if (fechaSeleccionada < ahora) {
      alert("La fecha y hora seleccionadas no pueden ser en el pasado.");
      return;
    }
  
    // Generar folio único
    const timestamp = Date.now();
    const folio = `CITA-${timestamp.toString(36).toUpperCase()}`;
  
    // Estructura de cita común
    const cita = {
      nombre,
      paterno,
      materno,
      especialista,
      fecha,
      hora,
    };
  
    // Guardar en la estructura correspondiente según modalidad
    if (modalidad === "en_linea") {

      // Asignar link de Zoom cuando es en línea
      cita.linkZoom = "https://zoom.us/j/1234567890"; // Link simulado
      citasEnLinea[folio] = cita;

      alert(`Cita en línea guardada con éxito. Tu folio es: ${folio}. Enlace de Zoom: ${cita.linkZoom}`);
    } 
    else if (modalidad === "presencial") {
      // Dependiendo del especialista, asignar el mensaje de contacto
      if (especialista === "Dr. Rodrigo Betancourt - Ginecología y Obstetricia") {
        cita.contacto = "El Dr. Rodrigo Betancourt se contactará para asignarte la clínica.";
      } 
      else if (especialista === "Dra. Angelica Resenediz - Ginecología, Obstetricia y Perinatología") {
        cita.contacto = "La Dra. Angelica Resenediz se contactará para asignarte la clínica.";
      }
      else if (especialista === "Dr. Damián Gutierrez - Ginecología y Neonatología") {
        cita.contacto = "El Dr. Damián Gutierrez se contactará para asignarte la clínica.";
      }
      else if (especialista === "Dra. Susana Moscoso - Ginecología y Consultora de Lactancia") {
        cita.contacto = "La Dra. Susana Moscoso se contactará para asignarte la clínica.";
      }

      citasPresenciales[folio] = cita;
      alert(`Cita presencial guardada con éxito. Tu folio es: ${folio}. ${cita.contacto}`);
    }
  
    // Limpiar el formulario después de agendar
    limpiarFormulario();
    console.log("Citas en línea actuales:", citasEnLinea);
    console.log("Citas presenciales actuales:", citasPresenciales);
  }
  
  // Función para limpiar el formulario
  function limpiarFormulario() {
    document.getElementById("citaForm").reset();  // Resetea todos los campos del formulario
    // También puedes limpiar manualmente los valores si es necesario:
    // document.getElementById("modalidad").value = "";
  }
  

// Función para buscar una cita por folio
function buscarCita() {
  const folioBusqueda = document.getElementById("folioBusqueda").value.trim();

  // Verificar si el folio no está vacío
  if (!folioBusqueda) {
    alert("Por favor, ingresa un folio.");
    return;
  }

  // Buscar la cita en el diccionario
  const cita = citas[folioBusqueda];

  if (cita) {
    alert(
      `Cita encontrada:\nNombre: ${cita.nombre} ${cita.paterno} ${cita.materno}\nEspecialista: ${cita.especialista}\nFecha: ${cita.fecha}\nHora: ${cita.hora}`
    );
    limpiarFormulario();
  }
  else {
    alert("No se encontró ninguna cita con ese folio.");
    limpiarFormulario();
  }
}

// Función para reagendar cita
function reagendarCita() {
    const folio = document.getElementById("folioReagendar").value.trim();
    const nuevaFecha = document.getElementById("fechaReagendar").value.trim();
    const nuevaHora = document.getElementById("horaReagendar").value.trim();
  
    // Validar campos
    if (!folio || !nuevaFecha || !nuevaHora) {
      alert("Por favor, completa todos los campos.");
      return;
    }
  
    // Validar si la cita existe
    if (!citas[folio]) {
      alert("No se encontró una cita con ese folio.");
      return;
    }
  
    // Depuración: Imprimir la nueva fecha y hora ingresada
    console.log("Nueva Fecha: " + nuevaFecha + ", Nueva Hora: " + nuevaHora);
  
    // Verificar si la nueva hora ya está ocupada en la misma fecha para otras citas (excepto la misma cita)
    for (let key in citas) {
      // Excluir la cita que estamos tratando de modificar
      if (key !== folio && citas[key].fecha === nuevaFecha && citas[key].hora === nuevaHora) {
        console.log(`Conflicto encontrado en la cita con folio: ${key}`);
        alert(`La hora ${nuevaHora} ya está ocupada en la fecha ${nuevaFecha}. Por favor, selecciona otra.`);
        return;
      }
    }
  
    // Actualizar los datos de la cita
    citas[folio].fecha = nuevaFecha;
    citas[folio].hora = nuevaHora;
  
    // Depuración: Mostrar el estado de las citas después de la actualización
    console.log("Citas actualizadas:", citas);
  
    alert(`La cita con folio ${folio} ha sido reagendada:\nNueva Fecha: ${nuevaFecha}\nNueva Hora: ${nuevaHora}`);
    
    // Limpiar el formulario después de reagendar
    limpiarFormulario();
  }
  
  
  

// Función para cancelar la acción de reagendar
function cancelarReagenda() {
  document.getElementById("reagendarForm").reset();
}

// Función para cancelar una cita
function cancelarCita() {
    const folio = document.getElementById("folioCancelar").value.trim();
    const motivo = document.getElementById("motivoCancelar").value.trim();
  
    // Validar que el folio no esté vacío
    if (!folio) {
      alert("Por favor, ingresa el folio de la cita.");
      return;
    }
  
    // Validar si la cita existe en el diccionario
    if (!citas[folio]) {
      alert("No se encontró una cita con ese folio.");
      return;
    }
  
    // Eliminar la cita del diccionario
    delete citas[folio];
  
    // Mostrar mensaje de éxito
    alert(`La cita con folio ${folio} ha sido cancelada.`);
    
    // Limpiar el formulario después de cancelar
    document.getElementById("cancelarForm").reset();
  }
