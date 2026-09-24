# Searching-for-a-repo-that-doesn-t-exist
I do stuff here assegemnt. B)

20/6/16 - srpint 3 thing ends. pls add more lol




Code from other people or the web i use :D

I lowkey use w3schools for everything :p 

Vedya and lily from my class help me and give some code stuff. :D


Navigation bar:
- https://www.w3schools.com/howto/howto_js_topnav.asp
- https://www.youtube.com/watch?v=f3uCSh6LIY0

Heading:
- https://www.w3schools.com/html/html_images_background.asp

display gird and like sum thing:
- https://www.youtube.com/watch?v=EaWj2AWI5Es - 8:36 must wacth
- https://cssgridgarden.com/
- https://css-tricks.com/almanac/properties/o/overflow-clip-margin/ 

Sign in and logn in page:
- https://www.w3schools.com/Tags/tryit.asp?filename=tryhtml5_input_type_text
- https://www.youtube.com/watch?v=2O8pkybH6po - brocode
- https://www.youtube.com/watch?v=qAR97gJX4yk -cs brain
- https://www.youtube.com/watch?v=lLc_jHkifRc - idk, i use this for form thing


DYAMICROUTES:
- https://www.youtube.com/watch?v=Jm38tqJRaK8 - Nick De Raj

FORM:
- https://github.com/MrWardKKHS/shepherd.git


------------------------->>>>>>>>>>>>>>>>>>


Textarea because i dont know what it is:
- https://www.w3schools.com/tags/tag_textarea.asp


CommonTasks folder thing i used and look at from SRCodeer:

Using Forms
DynamicRoutes
SimpleSessionLogin
ImageUp loads
SimpleUserLogin

Coding2go - youtube

---------------------------->>>>>>>>>>>>>>>>>>>>

PAST OF CODE! (THIS WILL BE GONE!!)

Flash - error thing

resulte {0} (give you the one you want/ user wise) 

if check_password_Hash(user[2]password):
session['user'] = user
flash('ppassjidsajd")



@app.route( '/make_Game' )
def make_Game():

    id = session["User"]['uuid']

    Title = request.form["Title"]
    About = request.form["About"]
    type_Genre = request.form["Genre"]

    filename = request.files["file"].filename
    file  = request.files["file"]

    file.save(UPLOAD_FOLDER / filename)

    return render_template('regGame.html')



3/8/26 -
- the "return redirect("/Game")" keep sending me back to thing. which is tycpially what it meant to do, but like doesn't say on page that the user need to sign in, only on the game page :p



add this in when im done
@app.route( '/regGame' )
def regGame():
    #this get the user session and make it to a varblae.
    user = session.get("User", None)
    if not user:
        flash("not log in :p", category ="warning")
