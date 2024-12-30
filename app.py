from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import pymysql
import hashlib

def InsertarUsuario(user, password):
    connection = pymysql.connect(host="localhost", user="root", password="", database="loginpython", port=3306,)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (User, password) VALUES (%s, %s)", (user, HashearPassword(password)))
    connection.commit()
    cursor.close()
    connection.close()

def ValidarUsuario(user, password):
    with pymysql.connect(host="localhost", user="root", password="", database="loginpython", port=3306) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE User = %s AND password = %s", (user, HashearPassword(password)))
            return cursor.fetchone() is not None
    
def HashearPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        valido = ValidarUsuario(user, password)
        
        if valido:
            return redirect(url_for('home'))    
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('login.html')
@app.route('/home')
def home():
    return render_template('home.html')
