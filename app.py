from flask import Flask , render_template, session, redirect, url_for, request

import sqlite3


app = Flask(__name__)

#radnon secry key for each session i think
app.config['SECRET_KEY'] = "SecretkeyXD"

DATABASE = "Database-1.db"

USERNAME = "Name"
PASSWORD = "Pass"

def query_db(sql,args=(),one=False):
    #connect and query- will retun one item if one=true and can accept arguments as tuple
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    #return None if ther is no result from the query
    #return the first item only if one=True
    #return the list of tuples if one=False
    return (results[0] if results else None) if one else results


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

#stuff of Dynamic Routes

@app.route('/User' )
def user():
    results = query_db("SELECT * FROM User")
    return render_template('User.html', results=results)

@app.route( '/User/<int:id>' )
def simple(id):
    sql = f"SELECT * FROM User WHERE id =?"
    User = query_db(sql, args=(id,), one=True)
    return render_template('simple_User.html', User=User)#give the data a templagte or like looks

@app.route( '/simple_User' )
def simple_User():
    return render_template('simple_User.html')

#End of Dynamic Routes

@app.route( '/Games' )
def Games():
    return render_template('Games.html')

@app.route( '/test' )
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)