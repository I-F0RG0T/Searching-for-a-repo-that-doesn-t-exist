from flask import Flask , render_template, session, redirect, url_for, request, flash
from livereload import Server
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path


app = Flask(__name__)

# This make the secrect key or harsh for each session random
app.config['SECRET_KEY'] = "SecretkeyXD"

# Connects to the Dataabse or SQL
DATABASE = "Data-1.db"

# Help put any images that the user want to put in to the folder.
UPLOAD_here = Path('static/UPLOAD')
PFP_UPLOAD = Path('static/UPLOAD/PFP')


def query_db(sql, args=(), one = False):
    """ Connect and query- will retun one item if one=true and can accept arguments as tuple """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


@app.route('/')# <-- this is the name of a page of this website! the ('/') is what it is refear too. 
def index():# <-- What this page do. OR like the 'definition' of a code.
    return render_template('index.html')
#This return this back to html it is assset too. the 'redner_template('index.html')' is telling
# the thing in the defense to go and let it procesee.

#Sign up!!

@app.route( '/signup', methods=["GET","POST"])#<-- the 'methods=["GET","POST"]' is saying that we are getting somehting from the html area and posting it.
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

        sql = "SELECT user_id, Username, Password from User WHERE Username = ?"
        User = query_db(sql=sql,args=(Username,),one=True)

        
        #v i think this is wrong!! 
        if User:
            #check the has and the password and see if it macth. It only works with thr hash one thought becasue the first user osnt hasrh and is working becasue of teh hasrd.
            if check_password_hash(User[2], Password):
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
    game = query_db(f"SELECT * FROM game LEFT JOIN Faves ON game.game_id = Faves.game_id LEFT JOIN Genre ON Game.game_id = Genre.id WHERE Faves.user_id = {user_id};")
  
    User = query_db(sql, one=True)
    if User == None:
        exit(404)
    
    return render_template('simple_User.html', User=User, game=game ) #give the data a templagte or like looks

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
    User = query_db(f"SELECT * FROM User INNER JOIN Faves ON User.user_id = Faves.user_id WHERE Faves.game_id = {game_id};")
    Genre = query_db(f"SELECT Genre.type FROM Genre LEFT JOIN Game on Game.type_Genre = Genre.id WHERE game_id = {game_id};")

    Game = query_db(sql, one=True)
    if Game == None:
        exit(404)

    return render_template('Game_info.html', Game=Game, User=User, Genre=Genre, )#give the data a templagte or like looks

def Game_list():
    return render_template('Game_info.html')

#End of Dynamic Routes Games ;,D | Start for making ur own game page!

@app.route( '/regGame')
def regGame():
    #this get the user session and make it to a varblae.

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
    
    sql = """
        INSERT INTO Game (Title, About, filename, type_Genre )
        VALUES (?, ?, ?, ?)
        """
    
    query_db(sql,(Title, About, filename, type_Genre ) )

    return redirect("/Game")

# Customs stuff! :D  

@app.route( '/custom' )
def custom():
    UserID = session['User']
     # 'user' is the persom in the session and id is the person ID in the yeah

    Game = query_db(f"SELECT * FROM Game;")
    Faves = query_db(f"SELECT Game.title, Genre.type, Faves.Review From Faves LEFT JOIN Game ON Faves.game_id = Game.game_id LEFT JOIN Genre ON Game.type_Genre = Genre.id WHERE Faves.user_id = {UserID[0]}")

    return render_template('custom.html', User=UserID, Game=Game, Faves=Faves)

@app.route( '/Like_Games', methods=["GET","POST"] )
def like_games():

    UserID = session['User'][0]
    game_id = request.form["game_id"]

    sql = """
        INSERT INTO Faves (user_id, game_id )
        VALUES (?, ? )
        """
    
    query_db(sql,(UserID, game_id ) )

    return redirect("/custom")

@app.route( '/Account', methods=["GET","POST"] )
def Account():

    UserID = session['User'] #Get which user is in the session ['user] and grabs their user id [0] from the Database. 
    Username = request.form["Username"]
    About = request.form["About"]

    pfp = request.files["pfp"]
    pfpname = request.files["pfp"].filename
    
    if pfp:
        pfp.save(PFP_UPLOAD / pfpname)

    sql = """
        UPDATE User SET Username = (Username), pfpname = (pfpname), About = (About) WHERE user_id = 3;
        VALUES (?, ?, ? )
        """
    
    query_db(sql,( Username, pfpname, About ) )

    return redirect("/custom")


# --------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



@app.route( '/help' )
def help():
    
    return render_template('help.html')

@app.route( '/404' )
def Error():
    
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)