from flask import Flask, render_template,redirect, url_for, request,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'signup'

mysql = MySQL(app)

app.secret_key = "hellome"

@app.route('/home')
def home():
    return render_template("home.html", email=session['email'])


@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form["name"]
        phone = request.form["phone"]
        email= request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO log VALUES (%s,%s,%s,%s)",(name,phone,email,password))
        cursor.connection.commit()
        cursor.close()
    return render_template("signup.html")

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM log WHERE email = %s AND password = %s",(email,password))
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['email'] = data[1]
            return redirect(url_for("home"))
        else:
            message = 'Inavlid h'
            print("Invalid ID/Pass")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)        
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()