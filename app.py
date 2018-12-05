import os

from flask import Flask, request, render_template, session, redirect, flash, url_for

from util import dbcommands as db, accounts, movies, books

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

@app.route('/book_info/<bookID>')
def book(bookID):
    data = books.google_books_data(bookID)
    # print(data)
    if(accounts.is_logged_in()):
        return render_template('book_info.html', dict=data,rec_list = books.book_rec(books.remove_nonascii(data.get("items")[0]["volumeInfo"]["title"].replace(" " , "+"))), bookID=bookID ,loggedIn=True, user=db.get_username(session["id"]))
    else:
        return render_template('book_info.html', dict=data,rec_list = books.book_rec(books.remove_nonascii(data.get("items")[0]["volumeInfo"]["title"].replace(" " , "+"))), bookID=bookID, loggedIn=False)

@app.route('/movie_info/<movieID>')
def movie(movieID):
    dict = movies.movie_info("&i=", movieID)
    recs = rec_list = movies.movie_rec(dict["Title"].replace(" " , "+"))
    print(recs)
    if(accounts.is_logged_in()):
        return render_template('movie_info.html',
                           **dict,
                           movieID=dict.get('imdbID'),
                           rec_list = recs,
                           loggedIn=True, user=db.get_username(session["id"]))
    else:
        return render_template('movie_info.html',
                           **dict,
                           movieID=dict.get('imdbID'),
                           rec_list = recs,
                           loggedIn=False)

@app.route('/search', methods=["GET"])
def search():
    type = request.args.get("type")
    query =request.args.get("query").replace(" " , "+")
    if(query==""):
        return redirect(url_for('index'))
    if(type == "Books"):
        return redirect(url_for('book_search', query=query))
    else:
        return redirect(url_for('movie_search', query=query))

@app.route('/book_search/<query>')
def book_search(query):
    if(query==""):
        return redirect(url_for('index'))
    data = books.google_books_data(query)
    if(accounts.is_logged_in()):
        return render_template('book_search.html', dict=data , query=query, loggedIn=True, user=db.get_username(session["id"]))
    else:
        return render_template('book_search.html', dict=data , query=query, loggedIn=False)

@app.route('/movie_search/<query>')
def movie_search(query):
    print("inside movie search")
    print(query)
    if(query==""):
        return redirect(url_for('index'))
    list = movies.better_movie_list(movies.movie_info("&s=", query).get("Search"))

    if(accounts.is_logged_in()):
        return render_template('movie_search.html',
                               query=query,
                               list=list,
                               loggedIn=True,
                               user=db.get_username(session["id"]))
    else:
        return render_template('movie_search.html', query=query, list=list, loggedIn=False)

if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()
