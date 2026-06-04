from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')

def base():
    return render_template('base.html')

@app.route( '/signin' )
def signin():
    return render_template('signin.html')

@app.route( '/post' )
def post():
    return render_template('post.html')

if __name__ == "__main__":
    app.run(debug=True)