from datetime import date
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, session
import pymysql
import pymysql.cursors
import hashlib

app = Flask(__name__)
app.secret_key = b'\x97\xa6\xe3?Bm\xdcL!I=\x08\xe96\x18\xd6q\x9bq\x83\xce8\xbd&'

def HashearPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def InsertarUsuario():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="taskmanager",
        port=3306,
    )
    
    cursor = connection.cursor()
    
    cursor.execute(
        """
        INSERT INTO Users (name, email, password_hash, create_date)
        VALUES (%s, %s, %s, %s)
        """,
        (
            "Jordy Moreno Arias",
            "yordimorenoarias.11@gmail.com",
            HashearPassword("2001892z"),
            date.today()
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

def obtenertareas(UserId): 
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
            cursor.execute("SELECT * FROM Tasks WHERE user_Id = %s", (UserId,))
            tareas = cursor.fetchall()
        return tareas
    finally:
        connection.close()

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
    
@app.route('/task', methods=['POST'])

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
                print(UserId)
                print(datos)
                cursor.execute(query, (
                    UserId, 
                    datos.get('titulo'), 
                    datos.get('descripcion'), 
                    datos.get('prioridad'), 
                    datos.get('categoria'), 
                    datos.get('fecha'), 
                    'En Proceso'
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
