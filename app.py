from flask import Flask , render_template, session, redirect, url_for, request

import sqlite3


app = Flask(__name__)

#radnon secry key for each session i think
app.config['SECRET_KEY'] = "SecretkeyXD"

DATABASE = "database-1.db"

USER: "Name"
PASS: "Pass"


@app.route('/')
def index():
    return render_template('index.html')

@app.route( '/signup' )
def signup():
    return render_template('signup.html')

@app.route( '/signin' )
def signin():
    return render_template('signin.html')

@app.route( '/post' )
def post():
    return render_template('post.html')

if __name__ == "__main__":
    app.run(debug=True)