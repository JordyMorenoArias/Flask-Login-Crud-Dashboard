from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)
app.secret_key = b'\x97\xa6\xe3?Bm\xdcL!I=\x08\xe96\x18\xd6q\x9bq\x83\xce8\xbd&'
import pymysql
import hashlib

def InsertarUsuario(user, password):
    connection = pymysql.connect(host="localhost", user="root", password="", database="loginpython", port=3306,)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (User, password) VALUES (%s, %s)", (user, HashearPassword(password)))
    connection.commit()
    cursor.close()
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

@app.route('/home')
def home():
    if 'IdUser' in session:
        IdUser = session['IdUser']
        return render_template('home.html', IdUser=IdUser)
    else:
        return redirect(url_for('Login'))
    

