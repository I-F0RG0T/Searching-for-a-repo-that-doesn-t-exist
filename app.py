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
        flash("You have Sign up!")
    return render_template('signup.html')


#Login :p

@app.route( '/Login', methods=["GET","POST"])
def Login(): 
    if request.method == "POST":

        Username = request.form['Username']
        Password = request.form['Password']

        sql = "SELECT Username, Password from User WHERE Username = ?"
        User = query_db(sql=sql,args=(Username,),one=True)

        
        #v i think this is wrong!! 
        if User:
            #check the has and the password and see if it macth. It only works with thr hash one thought becasue the first user osnt hasrh and is working becasue of teh hasrd.
            if check_password_hash(User[1], Password):
                session['User'] = User
                flash('You are sign in!')
                return redirect("/")
            else:
                flash('Something went wrong! Try again!')
        else:
            flash("You dont have a account with this!")

    return render_template('Login.html')

#Start of log out and end of Login

@app.route('/logout')
def logout():
    #just clear the username from the session and redirect back to the home page
    session['User'] = None
    flash("You have log out!")
    return redirect('/')


#Start of Dynamic Routes and end  of Log out

@app.route('/UserPage' )
def user():
    results = query_db("SELECT * FROM User")

    return render_template('UserPage.html', results=results)

@app.route( '/User/<int:user_id>' )
def User_list(user_id):
    sql = f"SELECT * FROM User WHERE user_id = {user_id}"
    gamefav = query_db(f"SELECT * FROM game INNER JOIN Faves ON game.game_id = Faves.game WHERE Faves.user_id = {user_id};")
  
    User = query_db(sql, one=True)
    if User == None:
        exit(404)
    return render_template('simple_User.html', User=User, gamefav=gamefav)#give the data a templagte or like looks

@app.route( '/simple_User' )
def simple_User():
    return render_template('simple_User.html')

#End of Dynamic Routes for User and start of Games ;,D

@app.route( '/Game', methods=["GET","POST"])
def Game():
    results = query_db("SELECT * FROM Game;")

#List of like genres. I didn't know how to make like sectiosn for genres unless it like this.
    Horror = query_db("SELECT * FROM Genre;")
    for Genre in Horror:
        Horror = query_db(f"SELECT * FROM Game WHERE Game.type_Genre = 1")
        #the quert_db for this one and the many under this is telling sql that it should grab the games
        #if they are in 'game-type_genre = [whatver number it is]'. which is the id of the genre type.

    Fsp = query_db("SELECT * FROM Game;")
    for Genre in Fsp:
        Fsp = query_db("SELECT * FROM Game WHERE Game.type_Genre = 2")

    Roleplaying = query_db("SELECT * FROM Genre;")
    for Genre in Roleplaying:
        Roleplaying = query_db("SELECT * FROM Game WHERE Game.type_Genre = 3")

    Adventure = query_db("SELECT * FROM Game;")
    for Genre in Adventure:
        Adventure = query_db("SELECT * FROM Game WHERE Game.type_Genre = 4")

    Rpg = query_db("SELECT * FROM Genre;")
    for Genre in Rpg:
        Rpg = query_db("SELECT * FROM Game WHERE Game.type_Genre = 5")
    
    Casical = query_db("SELECT * FROM Game;")
    for Genre in Casical:
        Casical = query_db("SELECT * FROM Game WHERE Game.type_Genre = 6")

    return render_template('Game.html', results=results, Horror=Horror, Fsp=Fsp, Roleplaying=Roleplaying, Adventure=Adventure, Rpg=Rpg, Casical=Casical )


#More games page related stiff. ------------------->>>>>>>....

@app.route( '/Game/<int:game_id>' )
def Game_list(game_id):
    sql = f"SELECT * FROM Game WHERE game_id = {game_id}"
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
    file = request.files["file"]
    filename = request.files["file"].filename

    if file:
        file.save(UPLOAD_here / filename)
    
    print(filename, file)
    sql = """
        INSERT INTO Game (Title, About, filename, type_Genre )
        VALUES (?, ?, ?, ?)
        """
    
    query_db(sql,(Title, About, filename, type_Genre ) )

    return redirect("/Game")

# stuff here --------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route( '/404' )
def Error():
    
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)