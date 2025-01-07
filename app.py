from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)
app.secret_key = b'\x97\xa6\xe3?Bm\xdcL!I=\x08\xe96\x18\xd6q\x9bq\x83\xce8\xbd&'
import pymysql
import pymysql.cursors
import hashlib

def InsertarUsuario(user, password):
    connection = pymysql.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="gestortareas", 
        port=3306,
    )
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (User, password) VALUES (%s, %s)", (user, HashearPassword(password)))
    connection.commit()
    cursor.close()
    connection.close()

def obtenertareas(IdUser): 
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="gestortareas",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Tareas WHERE IdUser = %s", (IdUser,))
            tareas = cursor.fetchall()
        return tareas
    finally:
        connection.close()

    
def HashearPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            return render_template('login.html', error="Los campos no pueden estar vacíos")
        
        with pymysql.connect(host="localhost", user="root", password="", database="loginpython", port=3306) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Id FROM Users WHERE User = %s AND Password = %s", (email, HashearPassword(password)))
                result = cursor.fetchone()
        
        if result:
            session['IdUser'] = result[0]
            return redirect(url_for('home'))    
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('login.html')

@app.route('/dashboard')
def home():
    if 'IdUser' in session:
        IdUser = session['IdUser']
        return render_template('dashboard.html', IdUser=IdUser)
    else:
        return redirect(url_for('Login'))
    
@app.route('/dashboard/tareas', methods=['POST'])
def crearTarea():
    if 'IdUser' in session:
        IdUser = session['IdUser']
        tarea = request.form['tarea']
        
        connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="gestortareas",
        port=3306)
