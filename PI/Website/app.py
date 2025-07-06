from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_mysqldb import MySQL
import MySQLdb
import re
from datetime import datetime

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'salud_materna'
app.secret_key = 'clave_secreta_salud_materna'

mysql = MySQL(app)

# Función para probar la conexión a la base de datos
def test_database_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return True, "Conexión exitosa a la base de datos"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

# Ruta para probar la conexión a la base de datos
@app.route('/test_db')
def test_db():
    success, message = test_database_connection()
    return f"<h1>Prueba de conexión a MySQL</h1><p>{message}</p>"


# RUTAS PRINCIPALES

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctores LIMIT 4")
        doctores_db = cursor.fetchall()
        return render_template('index.html', doctores=doctores_db)
    except Exception as e:
        flash(f'Error al cargar la página: {str(e)}', 'error')
        return render_template('index.html', doctores=[])
    finally:
        cursor.close()


@app.route('/especialistas')
def especialistas():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM doctores")
        doctores_db = cursor.fetchall()
        return render_template('especialistas.html', doctores=doctores_db)
    except Exception as e:
        flash(f'Error al cargar especialistas: {str(e)}', 'error')
        return render_template('especialistas.html', doctores=[])
    finally:
        cursor.close()

@app.route('/consejos')
def consejos():
    return render_template('consejos.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')


# SISTEMA DE CITAS
@app.route('/agendar')
def agendar():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para agendar una cita', 'error')
        return redirect(url_for('login'))

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM doctores")
        doctores = cursor.fetchall()
        return render_template("agendar.html", doctores=doctores, errores=None, valores=None)
    except Exception as e:
        flash(f'Error al cargar doctores: {str(e)}', 'error')
        return render_template("agendar.html", doctores=[], errores=None, valores=None)
    finally:
        cursor.close()


@app.route('/procesar_cita', methods=['POST'])
def procesar_cita():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para agendar citas', 'error')
        return redirect(url_for('login'))

    # Usamos los nombres exactos del formulario HTML
    id_doctor = request.form.get('cmbDoctor')
    fecha = request.form.get('txtFecha')
    hora = request.form.get('txtHora')
    modalidad = request.form.get('cmbModalidad')
    sintomas = request.form.get('txtSintomas')

    errores = {}

    # Validaciones
    if not id_doctor or not id_doctor.isdigit():
        errores['cmbDoctor'] = 'Selecciona un doctor válido'
    if not fecha:
        errores['txtFecha'] = 'La fecha es obligatoria'
    if not hora:
        errores['txtHora'] = 'La hora es obligatoria'
    if not modalidad or modalidad not in ['presencial', 'en_linea']:
        errores['cmbModalidad'] = 'Selecciona una modalidad válida'

    if errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM doctores")
            doctores_db = cursor.fetchall()
            return render_template('agendar.html', 
                                   doctores=doctores_db,
                                   errores=errores,
                                   valores=request.form)
        finally:
            cursor.close()

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO citas (id_usuario, id_doctor, fecha, hora, modalidad, sintomas, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
        """, (session['id_usuario'], id_doctor, fecha, hora, modalidad, sintomas))
        mysql.connection.commit()

        flash('Cita agendada exitosamente', 'success')
        return redirect(url_for('mis_citas'))
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al agendar cita: {str(e)}', 'error')
        return redirect(url_for('agendar'))
    finally:
        cursor.close()

@app.route('/mis_citas')
def mis_citas():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para ver tus citas', 'error')
        return redirect(url_for('login'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT c.*, d.nombre as doctor_nombre, d.especialidad 
            FROM citas c
            JOIN doctores d ON c.id_doctor = d.id_doctor
            WHERE c.id_usuario = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """, (session['id_usuario'],))
        citas = cursor.fetchall()
        return render_template('mis_citas.html', citas=citas)
    except Exception as e:
        flash(f'Error al cargar citas: {str(e)}', 'error')
        return render_template('mis_citas.html', citas=[])
    finally:
        cursor.close()

@app.route('/cancelar_cita/<int:id_cita>')
def cancelar_cita(id_cita):
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para cancelar citas', 'error')
        return redirect(url_for('login'))
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE citas 
            SET estado = 'cancelada' 
            WHERE id_cita = %s AND id_usuario = %s
        """, (id_cita, session['id_usuario']))
        mysql.connection.commit()
        
        if cursor.rowcount == 0:
            flash('No se pudo cancelar la cita', 'error')
        else:
            flash('Cita cancelada exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al cancelar cita: {str(e)}', 'error')
    finally:
        cursor.close()
    
    return redirect(url_for('mis_citas'))


@app.route('/citas')
def citas():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para acceder a las opciones de citas', 'error')
        return redirect(url_for('login'))
    return render_template('Citas.html')


# --- SISTEMA DE USUARIOS ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('Registro.html', errores={}, valores={})
    
    # Procesar el formulario POST
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    telefono = request.form.get('telefono', '').strip()
    
    errores = {}
    
    # Validaciones
    if not nombre:
        errores['nombre'] = 'Nombre es obligatorio'
    if not email:
        errores['email'] = 'Email es obligatorio'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        errores['email'] = 'Email no válido'
    if not password:
        errores['password'] = 'Contraseña es obligatoria'
    elif len(password) < 8:
        errores['password'] = 'La contraseña debe tener al menos 8 caracteres'
    if password != confirm_password:
        errores['confirm_password'] = 'Las contraseñas no coinciden'
    
    if errores:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': 'Error de validación',
                'errors': errores
            }), 400
        return render_template('Registro.html', 
                            errores=errores,
                            valores=request.form)
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            errores['email'] = 'Este email ya está registrado'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Email ya registrado',
                    'errors': errores
                }), 400
            return render_template('Registro.html', 
                                errores=errores,
                                valores=request.form)
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, telefono)
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, password, telefono))
        mysql.connection.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'redirect': url_for('login')})
        
        flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        mysql.connection.rollback()
        app.logger.error(f'Error en registro: {str(e)}')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': 'Error en el servidor'
            }), 500
        
        flash('Error al registrar usuario. Por favor intenta nuevamente.', 'error')
        return render_template('Registro.html', 
                            errores={},
                            valores=request.form)
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', errores={})
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    errores = {}
    
    if not email:
        errores['email'] = 'Email es obligatorio'
    if not password:
        errores['password'] = 'Contraseña es obligatoria'
    
    if errores:
        return render_template('login.html', 
                            errores=errores,
                            valores=request.form)
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario and usuario['password'] == password:
            session['id_usuario'] = usuario['id_usuario']
            session['nombre'] = usuario['nombre']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('perfil'))
        else:
            errores['general'] = 'Email o contraseña incorrectos'
            return render_template('login.html', 
                                errores=errores,
                                valores=request.form)
    except Exception as e:
        flash(f'Error al iniciar sesión: {str(e)}', 'error')
        return redirect(url_for('login'))
    finally:
        cursor.close()

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/contactar/<int:doctor_id>')
def contactar_doctor(doctor_id):
    """Muestra el formulario para contactar a un doctor específico"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT id_doctor, nombre, especialidad, email, 
                   telefono, direccion_consultorio as direccion, 
                   experiencia, foto
            FROM doctores 
            WHERE id_doctor = %s
        """, (doctor_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            abort(404)
            
        # Formatear datos para la plantilla
        doctor['image'] = f"imagenes/{doctor['foto']}" if doctor['foto'] else "imagenes/doctor_default.jpg"
        doctor['address'] = doctor.get('direccion', 'Dirección no disponible')
        
        return render_template('ContactaAdoctores.html', doctor=doctor)
    except Exception as e:
        flash(f'Error al cargar información del doctor: {str(e)}', 'error')
        return redirect(url_for('especialistas'))
    finally:
        cursor.close()

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """Procesa el formulario de contacto con doctores"""
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    try:
        doctor_id = int(request.form.get('doctor_id'))
        name = request.form.get('name', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        symptoms = request.form.get('symptoms', '').strip()
        
        # Validaciones
        if not all([doctor_id, name, lastname, email, symptoms]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('contactar_doctor', doctor_id=doctor_id))
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Por favor ingresa un email válido', 'error')
            return redirect(url_for('contactar_doctor', doctor_id=doctor_id))
        
        cursor = mysql.connection.cursor()
        
        # Verificar que el doctor existe
        cursor.execute("SELECT 1 FROM doctores WHERE id_doctor = %s", (doctor_id,))
        if not cursor.fetchone():
            flash('Doctor no encontrado', 'error')
            return redirect(url_for('especialistas'))
        
        # Insertar el contacto en la tabla contactos
        cursor.execute("""
            INSERT INTO contactos 
            (nombre, apellido, email, sintomas, id_doctor)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, lastname, email, symptoms, doctor_id))
        mysql.connection.commit()
        
        flash('Tu mensaje ha sido enviado. El doctor se pondrá en contacto contigo pronto.', 'success')
        return redirect(url_for('especialistas'))
    
    except ValueError:
        flash('ID de doctor inválido', 'error')
        return redirect(url_for('especialistas'))
    except Exception as e:
        mysql.connection.rollback()
        app.logger.error(f'Error al enviar contacto: {str(e)}')
        flash('Error al enviar el mensaje. Por favor intenta nuevamente.', 'error')
        return redirect(url_for('contactar_doctor', doctor_id=doctor_id if 'doctor_id' in locals() else 0))
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/doctor/contactos')
def ver_contactos_doctor():
    """Muestra los contactos recibidos por un doctor"""
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para ver esta página', 'error')
        return redirect(url_for('login'))
    
    try:
        # Verificar si el usuario es doctor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id_doctor FROM doctores WHERE email = %s", (session.get('email'),))
        doctor = cursor.fetchone()
        
        if not doctor:
            flash('Esta sección es solo para doctores', 'error')
            return redirect(url_for('perfil'))
        
        # Obtener los contactos para este doctor
        cursor.execute("""
            SELECT c.*, d.nombre as doctor_nombre 
            FROM contactos c
            JOIN doctores d ON c.id_doctor = d.id_doctor
            WHERE c.id_doctor = %s
            ORDER BY c.fecha_contacto DESC
        """, (doctor['id_doctor'],))
        contactos = cursor.fetchall()
        
        return render_template('doctor_contactos.html', contactos=contactos)
    except Exception as e:
        flash(f'Error al cargar contactos: {str(e)}', 'error')
        return redirect(url_for('perfil'))
    finally:
        cursor.close()

@app.route('/perfil')
def perfil():
    if 'id_usuario' not in session:
        flash('Debes iniciar sesión para ver tu perfil', 'error')
        return redirect(url_for('login'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (session['id_usuario'],))
        usuario = cursor.fetchone()
        
        cursor.execute("""
            SELECT c.*, d.nombre as nombre_doctor 
            FROM citas c
            JOIN doctores d ON c.id_doctor = d.id_doctor
            WHERE c.id_usuario = %s AND c.fecha >= CURDATE()
            ORDER BY c.fecha ASC, c.hora ASC
            LIMIT 3
        """, (session['id_usuario'],))
        citas = cursor.fetchall()
        
        cursor.execute("""
            SELECT c.*, d.nombre as nombre_doctor 
            FROM citas c
            JOIN doctores d ON c.id_doctor = d.id_doctor
            WHERE c.id_usuario = %s AND c.fecha < CURDATE()
            ORDER BY c.fecha DESC
            LIMIT 5
        """, (session['id_usuario'],))
        citas_pasadas = cursor.fetchall()
        
        return render_template('perfil.html', 
                            usuario=usuario, 
                            citas=citas,
                            citas_pasadas=citas_pasadas)
    except Exception as e:
        flash(f'Error al cargar perfil: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()

@app.route('/ver_mensajes')
def ver_mensajes_doctores():
    """Muestra todos los mensajes enviados a doctores (sin restricción de usuario)"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Consulta directa a la base de datos
        cursor.execute("""
            SELECT 
                c.id_contacto, 
                c.nombre, 
                c.apellido, 
                c.email, 
                c.sintomas, 
                c.fecha_contacto,
                d.nombre as doctor_nombre,
                d.especialidad
            FROM contactos c
            JOIN doctores d ON c.id_doctor = d.id_doctor
            ORDER BY c.fecha_contacto DESC
        """)
        
        mensajes = cursor.fetchall()
        return render_template('ver_mensajes.html', mensajes=mensajes)
        
    except Exception as e:
        print(f"Error al obtener mensajes: {str(e)}")
        return "Error al cargar los mensajes", 500
    finally:
        cursor.close()

# OTRAS RUTAS 
@app.route('/cancelar')
def cancelar():
    return render_template('cancelar.html')

@app.route('/consultar')
def consultar():
    return render_template('consultar.html')

@app.route('/reagendar')
def reagendar():
    return render_template('reagendar.html')

@app.route('/perfil_editar')
def perfil_editar():
    return render_template('perfil_editar')

# --- MANEJO DE ERRORES ---
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_servidor(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)