from datetime import date  # Para manejar y trabajar con fechas.
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import pymysql
import pymysql.cursors
import hashlib  # Biblioteca para aplicar algoritmos de hash como SHA-256.

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Clave secreta para gestionar sesiones de usuario de manera segura.
app.secret_key = b'\x97\xa6\xe3?Bm\xdcL!I=\x08\xe96\x18\xd6q\x9bq\x83\xce8\xbd&'

# Función para hashear contraseñas utilizando el algoritmo SHA-256.
def HashearPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Ruta para registrar un nuevo usuario.
@app.route('/record-user')
def RecordUser():
    try:
        datos = request.get_json  # Obtener datos JSON enviados en la solicitud.
        # Conexión a la base de datos MySQL.
        connection = pymysql.connect(host="localhost", user="root", password="", database="taskmanager", port=3306)
    
        with connection.cursor() as cursor:
            # Consulta SQL para insertar un nuevo usuario en la tabla Users.
            query = 'INSERT INTO Users (name, email, password_hash, create_date) VALUES (%s, %s, %s)'
    
            # Ejecutar la consulta con los datos proporcionados.
            cursor.execute(query, {
                datos.get('name'),
                datos.get('email'),
                HashearPassword(datos.get('password'))
            })

            connection.commit()  # Confirmar los cambios en la base de datos.
            return jsonify({
                'mensaje': 'Usuario registrado exitosamente',
                'id': cursor.lastrowid  # Retornar el ID del último registro insertado.
            }), 201         
    except Exception as e:
        # Manejo de errores y retorno de respuesta con código 500.
        return jsonify({
            'error': 'Error en el servidor',
            'mensaje': str(e)
        }), 500

# Ruta para manejar el inicio de sesión.
@app.route('/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':  # Si la solicitud es POST (inicio de sesión).
        email = request.form['email']  # Obtener el email del formulario.
        password = request.form['password']  # Obtener la contraseña del formulario.

        if not email or not password:  # Validación de campos vacíos.
            return render_template('login.html', error="Los campos no pueden estar vacíos")
        
        # Conexión a la base de datos MySQL.
        with pymysql.connect(host="localhost", user="root", password="", database="taskmanager", port=3306) as connection:
            with connection.cursor() as cursor:
                # Consulta para verificar las credenciales del usuario.
                cursor.execute("SELECT user_Id FROM users WHERE email = %s AND password_hash = %s;", 
                               (email, HashearPassword(password)))
                result = cursor.fetchone()  # Obtener el primer resultado.
        if result:  # Si las credenciales son válidas.
            session['IdUser'] = result[0]  # Guardar el ID de usuario en la sesión.
            return redirect(url_for('dashboard'))  # Redirigir al dashboard.
        else:
            # Retornar mensaje de error si las credenciales son incorrectas.
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('login.html')  # Renderizar la página de inicio de sesión.

# Ruta para el dashboard del usuario autenticado.
@app.route('/dashboard')
def dashboard():
    if 'IdUser' in session:  # Verificar si el usuario está autenticado.
        UserId = session['IdUser']  # Obtener el ID del usuario de la sesión.
        return render_template('dashboard.html', UserId=UserId)  # Renderizar el dashboard.
    else:
        return redirect(url_for('Login'))  # Redirigir al inicio de sesión si no está autenticado.

# Ruta para crear una nueva tarea.
@app.route('/create-Task', methods=['POST'])
def createTask():
    if 'IdUser' not in session:  # Verificar si el usuario está autenticado.
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        datos = request.get_json()  # Obtener datos JSON enviados en la solicitud.
        if not datos:  # Validar que los datos no estén vacíos.
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        UserId = session['IdUser']  # Obtener el ID del usuario de la sesión.

        # Conexión a la base de datos MySQL.
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="taskmanager",
            port=3306
        )

        try:
            with connection.cursor() as cursor:
                # Consulta para insertar una nueva tarea en la tabla Tasks.
                query = "INSERT INTO Tasks (user_Id, task_name, description, priority, category, expiration_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (
                    UserId, 
                    datos.get('task_name'), 
                    datos.get('description'), 
                    datos.get('priority'), 
                    datos.get('category'), 
                    datos.get('expiration_date'), 
                    'Pendiente'  # Estado inicial de la tarea.
                ))
                
                connection.commit()  # Confirmar los cambios en la base de datos.
                return jsonify({'mensaje': 'Tarea creada exitosamente'}), 201

        except Exception as e:
            connection.rollback()  # Revertir los cambios en caso de error.
            return jsonify({'error': 'Error al crear la tarea', 'mensaje': str(e)}), 500
            
        finally:
            connection.close()  # Cerrar la conexión a la base de datos.
            
    except Exception as e:
        # Manejo de errores generales y retorno de respuesta con código 500.
        return jsonify({'error': 'Error en el servidor', 'mensaje': str(e)}), 500

# Ruta para actualizar una tarea existente.
@app.route('/update-task', methods=['PUT'])
def updateTask():
    if 'IdUser' not in session:  # Verificar si el usuario está autenticado.
        return jsonify({'error' : 'Usuario no autenticado'}), 401
    
    datos = request.get_json()  # Obtener datos JSON enviados en la solicitud.
    UserId = session['IdUser']  # Obtener el ID del usuario de la sesión.

    if not datos:  # Validar que los datos no estén vacíos.
        return jsonify({'error' : 'No se recibieron datos'}), 400
    
    # Conexión a la base de datos MySQL.
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="taskmanager",
        port=3306
    )

    try: 
        with connection.cursor() as cursor:
            # Consulta para actualizar una tarea existente.
            query = "UPDATE tasks SET task_name = %s, description = %s, priority = %s, category = %s, expiration_date = %s, status = %s WHERE task_Id = %s AND User_Id = %s"
            cursor.execute(query, (
                datos.get('task_name'), 
                datos.get('description'), 
                datos.get('priority'), 
                datos.get('category'), 
                datos.get('expiration_date'), 
                datos.get('status'),
                datos.get('task_Id'),
                UserId
            ))
            
            connection.commit()  # Confirmar los cambios en la base de datos.
            return jsonify({'mensaje' : 'Tarea actualizada exitosamente'}), 200
            
    except Exception as e:
        connection.rollback()  # Revertir los cambios en caso de error.
        return jsonify({'error': 'Error al actualizar la tarea', 'mensaje': str(e)}), 500

    finally:
        connection.close()  # Cerrar la conexión a la base de datos.

@app.route('/delete-task', methods=['DELETE'])
def deteleTask():
    if 'IdUser' not in session:  # Verificar si el usuario está autenticado.
        return jsonify({'error': 'Usuario no autenticado'}), 401
        
    datos = request.get_json()

    try:
        # Conexión a la base de datos MySQL con cursores tipo diccionario.
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="taskmanager",
            port=3306,
        )

        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM tasks WHERE task_Id = %s", datos.get('task_Id'))
            connection.commit()
            return jsonify({'mensaje' : 'La tarea fue eliminada correctamente'}), 200
        
    except Exception as e:
        connection.rollback()  # Revertir los cambios en caso de error.
        return jsonify({'error': 'Error al actualizar la tarea', 'mensaje': str(e)}), 500
    finally:
        connection.close()  # Cerrar la conexión a la base de datos.

# Ruta para obtener todas las tareas del usuario autenticado.
@app.route('/get-tasks', methods=['GET'])
def getTasks():
    if 'IdUser' not in session:  # Verificar si el usuario está autenticado.
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    UserId = session['IdUser']  # Obtener el ID del usuario de la sesión.
    
    # Conexión a la base de datos MySQL con cursores tipo diccionario.
    connection = pymysql.connect(host="localhost", user="root", password="", database="taskmanager", port=3306, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener todas las tareas del usuario.
            cursor.execute("SELECT * FROM Tasks WHERE user_Id = %s", (UserId))
            tareas = cursor.fetchall()  # Obtener todas las tareas en formato de lista de diccionarios.
        return jsonify(tareas)  # Retornar las tareas como respuesta JSON.
    finally:
        connection.close()  # Cerrar la conexión a la base de datos.
