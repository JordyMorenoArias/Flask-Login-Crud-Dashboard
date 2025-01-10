from datetime import date
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, session
import pymysql
import pymysql.cursors
import hashlib

app = Flask(__name__)
app.secret_key = b'\x97\xa6\xe3?Bm\xdcL!I=\x08\xe96\x18\xd6q\x9bq\x83\xce8\xbd&'

def HashearPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def CreateUser():
#     connection = pymysql.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="taskmanager",
#         port=3306,
#     )
    
#     cursor = connection.cursor()
    
#     cursor.execute(
#         """
#         INSERT INTO Users (name, email, password_hash, create_date)
#         VALUES (%s, %s, %s, %s)
#         """,
#         (
            
#         )
#     )

#     connection.commit()
#     cursor.close()
#     connection.close()

@app.route('/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            return render_template('login.html', error="Los campos no pueden estar vacíos")
        
        with pymysql.connect(host="localhost", user="root", password="", database="taskmanager", port=3306) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_Id FROM users WHERE email = %s AND password_hash = %s;", (email, HashearPassword(password)))
                result = cursor.fetchone()
        if result:
            session['IdUser'] = result[0]
            return redirect(url_for('dashboard'))    
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'IdUser' in session:
        UserId = session['IdUser']
        return render_template('dashboard.html', UserId=UserId)
    else:
        return redirect(url_for('Login'))
    
@app.route('/insert-Task', methods=['POST'])
def createTask():
    if 'IdUser' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        UserId = session['IdUser']

        try:
            connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="taskmanager",
            port=3306
            )
            print("Conexión exitosa")           
        except Exception as e:
            print("Error en la conexión:", e)


        try:
            with connection.cursor() as cursor:

                query = "INSERT INTO Tasks (user_Id, task_name, description, priority, category, expiration_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                cursor.execute(query, (
                    UserId, 
                    datos.get('task_name'), 
                    datos.get('description'), 
                    datos.get('priority'), 
                    datos.get('category'), 
                    datos.get('expiration_date'), 
                    'Pendiente'
                ))
                
                connection.commit()
                return jsonify({
                    'mensaje': 'Tarea creada exitosamente',
                    'id': cursor.lastrowid
                }), 201

        except Exception as e:
            connection.rollback()
            return jsonify({
                'error': 'Error al crear la tarea',
                'mensaje': str(e)
            }), 500
            
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({
            'error': 'Error en el servidor',
            'mensaje': str(e)
        }), 500

@app.route('/update-task', methods=['PUT'])
def updateTask():
    if 'IdUser' not in session:
        return jsonify({'error' : 'Usuario no autenticado'}), 401
    
    datos = request.get_json()
    UserId = session['IdUser']

    if not datos:
        return jsonify({'error' : 'No se recibieron datos'}), 400
    
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="taskmanager",
        port=3306
    )

    try: 
        
        print(datos);

        with connection.cursor() as cursor:

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
            
            connection.commit()

            return jsonify({'mensaje' : 'Tarea actualizada exitosamente'}), 200
            
    except Exception as e:
        connection.rollback()
        return jsonify({
            'error': 'Error al actualizar la tarea',
            'mensaje': str(e)
        }), 500

    finally:
        connection.close()
        
@app.route('/get-tasks', methods=['GET'])
def getTasks():
    if 'IdUser' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    UserId = session['IdUser']
    
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="taskmanager",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Tasks WHERE user_Id = %s", (UserId))
            tareas = cursor.fetchall()
        return jsonify(tareas)
    finally:
        connection.close()