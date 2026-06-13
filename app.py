from flask import Flask , render_template, request,flash, session, redirect
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = "MyReallySecretKey"



DATABASE = "database-1.db"

def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
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

def base(): 
    return render_template('base.html')

@app.route( '/signin', methods=["GET","POST"] )
def signin():
#Connect to the datavase file
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    results = cursor.fetchall()
#End of the connecting database 
#testing sing up thing#
    if request.method == "POST":
        username = request.form['user']
        password = request.form['pass']
        #hash it with the cool secutiry function
        hashed_password = generate_password_hash(password)
        #write it as a new user to the database
        sql = "INSERT INTO user (username,password) VALUES (?,?)"
        query_db(sql,(username,hashed_password))
        #message flashes exist in the base.html template and give user feedback
        flash("Sign Up Successful")
    return render_template('signin.html', results=results) 

@app.route( '/lognin' )
def lognin():
    return render_template('lognin.html')

@app.route( '/post' )
def post():
    return render_template('post.html')

if __name__ == "__main__":
    app.run(debug=True)