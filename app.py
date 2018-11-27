import os

from flask import Flask, request, render_template, session, redirect, flash, url_for

from util import dbcommands as db, accounts

app = Flask(__name__)
app.secret_key = os.urandom(32)
#OMDb apikey=1891fe35

@app.route('/')
def index():
    if (accounts.is_logged_in()):
       return render_template('index.html', loggedIn=True, user=db.get_username(session["id"]) )
    return render_template('index.html' , loggedIn=False)

@app.route('/login')
def login():
    if (accounts.is_logged_in()):
        return redirect(url_for('index'))
    return render_template('login.html', success=False)

@app.route("/loginAuth" , methods = ["POST"])
def loginAuthenticate():
    '''Authenticates the username and password that the user has entered in the
    login page. If either one of them is wrong, then it tells them to try again.
    If they are correct, then it creates a session and redirects them to the homepage.'''
    return accounts.loginAuthentication()

@app.route('/signup')
def signup():
    if (accounts.is_logged_in()):
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route("/signupAuth", methods = ["POST"])
def signupAuthenticate():
    '''Checks if the username that the user registers with is at least
    four characters long and that the passwords that they entered twice
    are the same. If they aren't correct, then tell them to try again.
    If they are correct, create the account and redirect to the login.'''
    return accounts.signupAuthentication()

@app.route("/logout")
def logout():
    if(accounts.is_logged_in()):
        '''Deletes the current session and redirects back to login page.'''
        session.pop("id")
        return redirect(url_for("index"))
    return redirect(url_for('index'))


@app.route('/book_info/<int:bookID>')
def book(bookID):
    return render_template('book_info.html')

@app.route('/movie_info/<int:movieID>')
def movie(movieID):
    return render_template('movie_info.html')


if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()
