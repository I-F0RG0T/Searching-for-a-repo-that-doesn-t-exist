from flask import Flask , render_template, session, redirect, url_for, request, flash
from livereload import Server
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path



app = Flask(__name__)

#radnon secry key for each session i think
app.config['SECRET_KEY'] = "SecretkeyXD"

DATABASE = "Data-1.db"

UPLOAD_here = Path('static/UPLOAD') 


def query_db(sql,args=(),one=False):
    #connect and query- will retun one item if one=true and can accept arguments as tuple
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute(sql, args)
    
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

@app.route('/')
def index():
    return render_template('index.html')

#Sign up!!

@app.route( '/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":

        Username = request.form['Username']
        Password = request.form['Password']

        hashed_password = generate_password_hash(Password)

        sql = "INSERT INTO User (Username, Password) VALUES (?,?)"
        query_db(sql,(Username, hashed_password))
        flash("signup goood")
    return render_template('signup.html')


#Login :p

@app.route( '/Login', methods=["GET","POST"])
def Login(): 
    if request.method == "POST":

        Username = request.form['Username']
        Password = request.form['Password']

        print("test tes ttes")
        print(Username)

        sql = "SELECT * from User WHERE Username = ?"
        Username = query_db(sql=sql,args=(Username,),one=True)

        print("help help")
        print(Username)
        
        #v i think this is wrong!! 
        if Username:
            if check_password_hash(Username[2],Password):#check the password thing. i think is worng
                session['Username'] = Username
                flash('Sign in good!!')
            else:
                flash('Wrong password!! try again! :^')
        else:
            flash("You dont have a account with this!")

    return render_template('Login.html')

#Start of log out and end of Login

@app.route('/logout')
def logout():
    #just clear the username from the session and redirect back to the home page
    session['User'] = None
    return redirect('/')


#Start of Dynamic Routes and end  of Log out

@app.route('/UserPage' )
def user():
    results = query_db("SELECT * FROM User")

    return render_template('UserPage.html', results=results)

@app.route( '/User/<int:id>' )
def User_list(id):
    sql = f"SELECT * FROM User WHERE id = {id}"
    GaTitle = query_db("SELECT Title FROM Game")

    User = query_db(sql, one=True)
    if User == None:
        exit(404)
    return render_template('simple_User.html', User=User, GaTitle=GaTitle)#give the data a templagte or like looks

@app.route( '/simple_User' )
def simple_User():
    return render_template('simple_User.html')

#End of Dynamic Routes for User and start of Games ;,D

@app.route( '/Game', methods=["GET","POST"])
def Game():
    results = query_db("SELECT * FROM Game ORDER BY type_Genre, Title GLOB '[A-Z,a-z]*' DESC;")
    test = query_db("""SELECT id, type FROM Genre ORDER BY type""")

    print(Game)

    return render_template('Game.html', results=results)


#idk what this is for lol
@app.route( '/test')
def test():
    test = query_db("""SELECT id, type FROM Genre ORDER BY type""")
    return redirect("/Game", test=test)

#More games page related stiff. ------------------->>>>>>>....

@app.route( '/Game/<int:id>' )
def Game_list(id):
    sql = f"SELECT * FROM Game WHERE id = {id}"

    User = query_db("SELECT * FROM User")

    Game = query_db(sql, one=True)
    if Game == None:
        exit(404)


    return render_template('Game_info.html', Game=Game, User=User)#give the data a templagte or like looks

def Game_list():
    return render_template('Game_info.html')

#End of Dynamic Routes Games ;,D | Start for making ur own game page!

@app.route( '/regGame')
def regGame():
    #this get the user session and make it to a varblae.

    #add the thing about the session :D

    type_Genre = query_db(""" SELECT id, type FROM Genre ORDER BY type """)

    return render_template('regGame.html', type_Genre=type_Genre)

@app.route( '/make_Game', methods=["GET","POST"] )
def make_Game():

    Title = request.form["Title"]
    About = request.form["About"]
    type_Genre = request.form["type_Genre"]
    wesbite_url = request.form["website_url"]

    file = request.files["file"]
    filename = request.files["file"].filename

    if file:
        file.save(UPLOAD_here / filename)

    sql = """
        INSERT INTO Game (Title, About, filename, type_Genre, wesbite_url)
        VALUES (?, ?, ?, ?, ?)
        """
    
    query_db(sql,(Title, About, filename, type_Genre, wesbite_url) )

    return redirect("/Game")

# stuff here --------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route( '/404' )
def Error():
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)