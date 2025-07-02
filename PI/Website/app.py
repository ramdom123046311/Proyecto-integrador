from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = 'manuel'  

# Diccionario datos de doctores
doctores = {
    'rodrigo': {
        'id': 'rodrigo',
        'name': 'Dr. Rodrigo Betancourt',
        'image': 'imagenes/drrodrigo.jfif',
        'twitter': '@docrod_beta',
        'phone': '442-311-2230',
        'email': 'rodri.betan@gmail.com',
        'address': 'Prol. Bernardo Quintana 2906, Cerrito Colorado, 76116 Santiago de Qro, Qro'
    },
    'angelica': {
        'id': 'angelica',
        'name': 'Dra. Angélica Resendiz',
        'image': 'imagenes/draange.png',
        'phone': '442-555-1234',
        'email': 'angelica.resendiz@example.com',
        'address': 'Hospital Los Angeles'
    },
    'damian': {
        'id': 'damian',
        'name': 'Dr. Damián Gutierrez',
        'image': 'imagenes/drdam.png',
        'phone': '442-555-5678',
        'email': 'damian.gutierrez@example.com',
        'address': 'Hospital del Niño y la Mujer en Qro'
    },
    'susana': {
        'id': 'susana',
        'name': 'Dra. Susana Moscoso',
        'image': 'imagenes/drasusana.png',
        'phone': '442-555-9012',
        'email': 'susana.moscoso@example.com',
        'address': 'Hospital General de Qro'
    }
}

# Mi Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/especialistas')
def especialistas():
    return render_template('especialistas.html')

@app.route('/consejos')
def consejos():
    return render_template('consejos.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

@app.route('/agendar')
def agendar():
    return render_template('agendar_citas.html')

@app.route('/registro')
def registro():
    return render_template('Registro.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# Página para cancelar citas
@app.route('/cancelar')
def cancelar():
    return render_template('cancelar.html')

# Contacto general
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Sistema de contacto con doctores
@app.route('/contactar/<doctor_id>')
def contactar_doctor(doctor_id):
    doctor = doctores.get(doctor_id)
    if not doctor:
        abort(404)
    return render_template('ContactaAdoctores.html', doctor=doctor)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    doctor_id = request.form.get('doctor_id')
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    symptoms = request.form.get('symptoms')
    
    # Aqui proceso el formulario para la base de datos
    print(f"\n--- Nuevo mensaje de contacto ---")
    print(f"Doctor: {doctores[doctor_id]['name']}")
    print(f"Paciente: {name} {lastname}")
    print(f"Email: {email}")
    print(f"Síntomas/Comentarios: {symptoms}\n")
    
    flash('Tu mensaje ha sido enviado. El doctor se pondrá en contacto contigo pronto.', 'success')
    return redirect(url_for('index'))

@app.route('/consultar')
def consultar():
    return render_template('consultar.html')

@app.route('/reagendar')
def reagendar():
    return render_template('reagendar.html')

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))
        
        
        flash('Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
