from flask import Flask , render_template, session, redirect, url_for, request

import sqlite3


app = Flask(__name__)

#radnon secry key for each session i think
app.config['SECRET_KEY'] = "SecretkeyXD"

DATABASE = "database-1.db"

USERNAME = "Name"
PASSWORD = "Pass"


@app.route('/')
def index():
    return render_template('index.html')

@app.route( '/signup' )
def signup():
    return render_template('signup.html')

@app.route( '/signup', methods=["GET","POST"])
def signup_post():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect("test")
    return render_template('signup.html')


@app.route( '/signin' )
def signin():
    return render_template('signin.html')


@app.route( '/test' )
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)