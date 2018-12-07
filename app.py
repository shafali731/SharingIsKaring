import os, random

from flask import Flask, request, render_template, session, redirect, flash, url_for

from util import dbcommands as db, accounts, movies, books

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    '''Renders the homepage for users who are both logged in
    and logged out. If user is logged in, displays recommendations
    based on movies added to watched and books added to read.'''
    if (accounts.is_logged_in()):
        watch = db.get_movies_watched(session['id'])
        # print("watched")
        # print(watch)
        data = []
        total = 0
        read = db.get_books_read(session['id'])
        data_books = []
        try:
            for id in watch:
                rec = movies.movie_rec("&q=movie:", movies.name_from_id(id).replace(" " , "+"))
                data.append(random.choice(rec))
        except :
            print("tastedive not working for movies")
        try:
            for id in read:
                rec_books = books.book_rec(books.name_from_id(id).replace(" " , "+"))
                data_books.append(random.choice(rec_books))
        except :
            print("tastedive not working for books")
        # print(data)
        # print(total)
        return render_template('index.html', loggedIn=True, user=db.get_username(session["id"]), recs_lists=data, recs_lists_books=data_books)
    return render_template('index.html' , loggedIn=False)

@app.route('/login')
def login():
    '''Displays the login page if user is not already logged in. Otherwise,
    redirects the user to homepage.'''
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
    '''Displays the signup page if user is not already logged in. Otherwise,
    redirects the user to homepage.'''
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
    '''Deletes the current session and redirects back to login page.'''
    if(accounts.is_logged_in()):
        session.pop("id")
        return redirect(url_for("login"))
    return redirect(url_for('index'))

@app.route('/book_info/<bookID>')
def book(bookID):
    '''Displays detailed information about a specific book based on
    the book's google book id. If tastedive offers recommendations for similar books,
    then it displays book recommendations'''
    data = books.google_books_data(bookID)
    # print(data)
    try:
        if(accounts.is_logged_in()):
            alreadyRead = db.get_books_read(session["id"])
            read = bookID in alreadyRead
            wishToRead = db.get_books_wishlist(session["id"])
            wish = bookID in wishToRead
            return render_template('book_info.html', dict=data,rec_list = books.book_rec(books.remove_nonascii(data.get("items")[0]["volumeInfo"]["title"].replace(" " , "+"))), bookID=bookID ,loggedIn=True, user=db.get_username(session["id"]), in_read = read, in_wish = wish)
        else:
            return render_template('book_info.html', dict=data,rec_list = books.book_rec(books.remove_nonascii(data.get("items")[0]["volumeInfo"]["title"].replace(" " , "+"))), bookID=bookID, loggedIn=False)
    except:
        return redirect(url_for('index'))

@app.route('/movie_info/<movieID>')
def movie(movieID):
    '''Displays detailed information about a specific movie based on
    the movie's imdb id. If tastedive offers recommendations for similar movies,
    then it displays movie recommendations'''
    dict = movies.movie_info("&i=", movieID)
    recs = []
    recs = rec_list = movies.movie_rec("&q=movie:", dict["Title"].replace(" " , "+"))
    # print(recs)
    if(accounts.is_logged_in()):
        alreadyWatched = db.get_movies_watched(session["id"])
        watched = movieID in alreadyWatched
        wishToWatch = db.get_movies_wishlist(session["id"])
        wish = movieID in wishToWatch
        return render_template('movie_info.html',
                           **dict,
                           movieID=dict.get('imdbID'),
                           rec_list = recs,
                           loggedIn=True, user=db.get_username(session["id"]),
                           in_watched = watched,
                           in_wish = wish
                           )
    else:
        return render_template('movie_info.html',
                           **dict,
                           movieID=dict.get('imdbID'),
                           rec_list = recs,
                           loggedIn=False)

@app.route('/search', methods=["GET"])
def search():
    '''If search query is for books, then redirects to book_search.
    If search query is for books, then redirects to movie_search.'''
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
    '''Displays book results for search query using google books api.
    If no results are found, displays no results message.'''
    if(query==""):
        return redirect(url_for('index'))
    data = books.google_books_data(query)
    if(accounts.is_logged_in()):
        return render_template('book_search.html', dict=data , query=query, loggedIn=True, user=db.get_username(session["id"]))
    else:
        return render_template('book_search.html', dict=data , query=query, loggedIn=False)

@app.route('/movie_search/<query>')
def movie_search(query):
    '''Displays movie results for search query using OMDB api.
    If no results are found, displays no results message.'''
    # print("inside movie search")
    # print(query)
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

@app.route("/alreadyRead" , methods=["GET"])
def render_read():
    '''Adds a specific book to the readORWatched table in the
    database'''
    id = request.args.get("ID")
    db.add_read(session["id"] ,id)
    return redirect(url_for('book' , bookID = id))

@app.route("/wishToRead" , methods=["GET"])
def render_read_wishlist():
    '''Adds a specific book to the wishlist table in the
    database'''
    id = request.args.get("ID")
    db.add_wishlist_book(session["id"] ,id)
    return redirect(url_for('book' , bookID = id))

@app.route("/alreadyWatched" , methods=["GET"])
def render_watched():
    '''Adds a specific movie to the readORWatched table in the
    database'''
    id = request.args.get("ID")
    db.add_watched(session["id"] ,id)
    return redirect(url_for('movie' , movieID = id))

@app.route("/wishToWatch" , methods=["GET"])
def render_watch_wishlist():
    '''Adds a specific movie to the readORWatched table in the
    database'''
    id = request.args.get("ID")
    db.add_wishlist_movie(session["id"] ,id)
    return redirect(url_for('movie' , movieID = id))

@app.route("/removeReadBook" , methods=["GET"])
def remove_book_readOrwatched():
    '''removes a specific book from the readORWatched table in the
    database'''
    id = request.args.get("ID")
    db.remove_book_read(session["id"], id)
    return redirect(url_for('book' , bookID = id))

@app.route("/removeWishBook" , methods=["GET"])
def remove_book_wishlist():
    '''removes a specific book from the wishlist table in the
    database'''
    id = request.args.get("ID")
    # print(id)
    db.remove_book_wish(session["id"], id)
    return redirect(url_for('book' , bookID = id))

@app.route("/removeWatchedMovie" , methods=["GET"])
def remove_movie_readOrwatched():
    '''removes a specific movie from the readORWatched table in the
    database'''
    id = request.args.get("ID")
    db.remove_movie_watched(session["id"], id)
    return redirect(url_for('movie' , movieID = id))

@app.route("/removeWishMovie" , methods=["GET"])
def remove_movie_wishlist():
    '''removes a specific movie from the wishlist table in the
    database'''
    id = request.args.get("ID")
    db.remove_movie_wish(session["id"], id)
    return redirect(url_for('movie' , movieID = id))

@app.route("/profile" , methods=["GET"])
def read_list():
    '''Displays a profile page for users where they
    can view the books they marked as read'''
    if(accounts.is_logged_in()):
       read=db.get_books_read(session['id'])
       data=[]
       try:
           for id in read:
               temp = books.google_books_data(id)
               if "items" in temp:
                   data.append(temp["items"][0])
               else:
                   continue
       except:
            print("error")
       return render_template("user_books.html", data=data , title="Books Read", no_results="Looks Like You Haven't Read Any Books",
                               loggedIn=True, user=db.get_username(session["id"]))
    else:
       return redirect(url_for('login'))

@app.route("/bookwish" , methods=["GET"])
def read_wishlist():
    '''Displays a profile page for users where they
    can view the books they wish to read'''
    if(accounts.is_logged_in()):
       read=db.get_books_wishlist(session['id'])
       data=[]
       try:
           for id in read:
               temp = books.google_books_data(id)
               if "items" in temp:
                   data.append(temp["items"][0])
               else:
                   continue
       except:
           print("error")
       return render_template("user_books.html", data=data , title="Want To Read", no_results="Looks Like You Don't Have Any Books Added",
                               loggedIn=True, user=db.get_username(session["id"]))
    else:
       return redirect(url_for('login'))

@app.route("/movieWatched" , methods=["GET"])
def watch_list():
    '''Displays a profile page for users where they
    can view the movies they marked as watched'''
    if(accounts.is_logged_in()):
       watch=db.get_movies_watched(session['id'])
       data=[]
       try:
           for id in watch:
               data.append(movies.movie_info("&i=" , id))
       except:
           print("error")
       return render_template("user_movies.html", data=data , title="Movies Watched", no_results="Looks Like You Haven't Watched Any Movies",
                               loggedIn=True, user=db.get_username(session["id"]))
    else:
       return redirect(url_for('login'))

@app.route("/moviewish" , methods=["GET"])
def watch_wishlist():
    '''Displays a profile page for users where they
    can view the movies they wish to watch'''
    if(accounts.is_logged_in()):
       watch=db.get_movies_wishlist(session['id'])
       # print(watch)
       data=[]
       try:
           for id in watch:
               data.append(movies.movie_info("&i=" , id))
       except:
           print("error")
       # print(data)
       return render_template("user_movies.html", data=data , title="Want To Watch", no_results="Looks Like You Don't Have Any Movies Added",
                               loggedIn=True, user=db.get_username(session["id"]))
    else:
       return redirect(url_for('login'))



if __name__ == '__main__':
    app.debug = False  # Set to `False` before release
    app.run()
