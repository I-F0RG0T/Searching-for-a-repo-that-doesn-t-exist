from flask import Flask, render_template, session, redirect, url_for, request, flash
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


def query_db(sql, args=(), one=False):
    """Connect and query.

    This will retun one item if one=true.

    It can accept arguments as tuple.
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    print(sql)
    print(args)

    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return ((results[0] if results else None) if one else results)


@app.route('/')
# this is the name of a page of this website!
# The ('/') is what it is refear too.
def index():
    """Run page."""
    # What this page do. OR like the 'definition' of a code.
    return render_template('index.html')
# This return this back to html it is assset too.
# The 'redner_template('index.html')' is telling
# the thing in the defense to go and let it procesee.

# Sign up!!


@app.route('/signup', methods=["GET", "POST"])
# the 'methods=["GET","POST"]' is saying that we are getting something
# from the html area and posting it.
def signup():
    """Run page and put new users username and password to the database."""
    if request.method == "POST":

        username = request.form['Username']
        password = request.form['Password']

        hashed_password = generate_password_hash(password)

        sql = "INSERT INTO User (Username, Password) VALUES (?,?)"
        query_db(sql, (username, hashed_password))
        flash("You have Sign up!")
    return render_template('signup.html')


# Login :p

@app.route('/Login', methods=["GET", "POST"])
def login():
    """Run page and grab the user informantion in database and checks it."""
    if request.method == "POST":

        Username = request.form['Username']
        Password = request.form['Password']

        sql = "SELECT user_id, Username, Password from User WHERE Username = ?"
        User = query_db(sql=sql, args=(Username), one=True)

        if User:
            # Check the has and the password and see if it match.
            # It only works with the hash one thought becasue the
            # first user osnt hasrh and is working becasue of the harsh.
            if check_password_hash(User[2], Password):
                session['User'] = User
                flash('You are sign in!')
                return redirect("/")
            else:
                flash('Something went wrong! Try again!')
        else:
            flash("You dont have a account with this!")

    return render_template('Login.html')

# Start of log out and end of Login


@app.route('/logout')
def logout():
    """Just clear the user session and redirect to the about page."""
    session['User'] = None
    flash("You have log out!")
    return redirect('/')


# Start of Dynamic Routes and end of Log out.


@app.route('/UserPage')
def user():
    """Run a page."""
    results = query_db("SELECT * FROM User")
    return render_template('UserPage.html', results=results)


@app.route('/User/<int:user_id>')
def user_list(user_id):
    """Returs this as muplitle pages for how many games is in the database."""
    sql = f"SELECT * FROM User WHERE user_id = {user_id}"
    game = query_db(f"SELECT * FROM game LEFT JOIN Faves ON game.game_id = Faves.game_id LEFT JOIN Genre ON Game.game_id = Genre.id WHERE Faves.user_id = {user_id};")
    user = query_db(sql, one=True)
    if user is None:
        exit(404)

    return render_template('simple_User.html', User=user, game=game)
    # give the data a templagte or like looks.


@app.route('/simple_User')
def simple_user():
    """Run game page."""
    return render_template('simple_User.html')

# End of Dynamic Routes for User and start of Games ;,D


@app.route('/Game', methods=["GET", "POST"])
def game():
    """Run the page and send data from the database."""
    results = query_db("SELECT * FROM Game;")

# List of genres.
    horror = query_db("SELECT * FROM Genre;")
    for genre in horror:
        horror = query_db("SELECT * FROM Game WHERE Game.type_Genre = 1")
        # the quert_db for this one and the many under this is telling
        # sql that it should grab the games if they are in
        # 'game-type_genre = [whatver number it is]'.
        # which is the id of the genre type.

    fsp = query_db("SELECT * FROM Game;")
    for genre in fsp:
        fsp = query_db("SELECT * FROM Game WHERE Game.type_Genre = 2")

    roleplaying = query_db("SELECT * FROM Genre;")
    for genre in roleplaying:
        roleplaying = query_db("SELECT * FROM Game WHERE Game.type_Genre = 3")

    adventure = query_db("SELECT * FROM Game;")
    for genre in adventure:
        adventure = query_db("SELECT * FROM Game WHERE Game.type_Genre = 4")

    rpg = query_db("SELECT * FROM Genre;")
    for genre in rpg:
        rpg = query_db("SELECT * FROM Game WHERE Game.type_Genre = 5")

    casical = query_db("SELECT * FROM Game;")
    for genre in casical:
        casical = query_db("SELECT * FROM Game WHERE Game.type_Genre = 6")

    return render_template('Game.html', results=results,
                           Horror=horror, Fsp=fsp,
                           Roleplaying=roleplaying, Adventure=adventure,
                           Rpg=rpg, Casical=casical)


# More games page related stiff. ------------------->>>>>>>


@app.route('/Game/<int:game_id>')
def game_list(game_id):
    """Run muplitle pages for how many games is in the database."""
    sql = f"SELECT * FROM Game WHERE game_id = {game_id}"
    user = query_db(f"SELECT * FROM User INNER JOIN Faves ON User.user_id = Faves.user_id WHERE Faves.game_id = {game_id};")
    genre = query_db(f"SELECT Genre.type FROM Genre LEFT JOIN Game on Game.type_Genre = Genre.id WHERE game_id = {game_id};")

    game = query_db(sql, one=True)
    if game is None:
        exit(404)

    return render_template('Game_info.html', Game=game,
                           User=user, Genre=genre)
    # give the data a templagte or like looks.

# End of Dynamic Routes Games ;,D | Start for making ur own game page!


@app.route('/regGame')
def reggame():
    """For the page to run and to get data from the database."""
    type_genre = query_db(""" SELECT id, type FROM Genre ORDER BY type """)

    return render_template('regGame.html', type_Genre=type_genre)


@app.route('/make_Game', methods=["GET", "POST"])
def make_game():
    """Add the user games into the data base."""
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

    query_db(sql, (Title, About, filename, type_Genre))

    return redirect("/Game")

# Likes stuff! :D


@app.route('/custom')
def custom():
    """Return some data from the database."""
    userid = session['User']
    # 'user' is the persom in the session and id
    # is the person ID in the database.

    game = query_db("SELECT * FROM Game;")
    faves = query_db(f"SELECT Game.title, Genre.type, Faves.Review From Faves LEFT JOIN Game ON Faves.game_id = Game.game_id LEFT JOIN Genre ON Game.type_Genre = Genre.id WHERE Faves.user_id = {userid[0]}")

    return render_template('custom.html', UserID=userid,
                           Game=game, Faves=faves)


@app.route('/Like_Games', methods=["GET", "POST"])
def like_games():
    """Run the user id and the game id into sql."""
    userid = session['User'][0]
    game_id = request.form["game_id"]

    sql = """
        INSERT INTO Faves (user_id, game_id )
        VALUES (?, ? )
        """
    query_db(sql, (userid, game_id))

    return redirect("/custom")


@app.route('/Account', methods=["GET", "POST"])
def account():
    """Update informantion of the user row."""

    UserID = session['User'][0]
    # Get which user is in the session ['user] and grabs
    # their user id [0] from the Database.
    Username = request.form["Username"]
    About = request.form["About"]

    pfp = request.files["pfp"]
    pfpname = request.files["pfp"].filename
    
    if pfp:
        pfp.save(PFP_UPLOAD / pfpname)

    sql = """
        UPDATE User SET Username = (Username), pfpname = (pfpname), About = (About) WHERE user_id = ?;
        VALUES (?, ?, ? )
        """

    print(UserID)

    query_db(sql,( Username, pfpname, About ) )

    return redirect("/custom")


# --------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


@app.route('/help')
def help():
    """Let the page run."""
    return render_template('help.html')


@app.errorhandler(404)
def error(error):
    """If put an mistake in the url or in general. It will direct here."""
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
