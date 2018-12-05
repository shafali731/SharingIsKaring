#util commands for messing with the database
import sqlite3
DB_FILE ="data/database.db"
#----------------when you want to add data to the database------------------------------
#adds to the users table
def add_user(username,password_hash):
    '''adds users to use table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO users (username,password_hash)VALUES(?,?);"
    c.execute(command,(username,password_hash))
    db.commit()
    db.close()

def add_read(userID,ID):
    '''adds books to readORwatched table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO readORwatched(userID,ID,type)VALUES(?,?,?);"
    c.execute(command,(userID, ID, "book"))
    db.commit()
    db.close()

def add_watched(userID,ID):
    '''adds movies to readORwatched table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO readORwatched(userID,ID,type)VALUES(?,?,?);"
    c.execute(command,(userID, ID, "movie"))
    db.commit()
    db.close()

def add_wishlist_book(userID,ID):
    '''adds books to wishlist table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO wishlist(userID, ID, type)VALUES(?,?,?);"
    c.execute(command,(userID, ID, "book"))
    db.commit()
    db.close()

def add_wishlist_movie(userID,ID):
    '''adds movies to wishlist table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO wishlist(userID, ID, type)VALUES(?,?,?);"
    c.execute(command,(userID, ID, "movie"))
    db.commit()
    db.close()

def get_books_read(userID):
    '''gets books from readORwatched based on userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT ID FROM readORwatched WHERE userID = ? AND type = ?;"
    c.execute(command,(userID, "book"))
    books = c.fetchall()
    # print(books)
    db.close()
    list = []
    for id in books:
        list.append(id[0])
    # print(list)
    return list

def get_movies_watched(userID):
    '''gets movies from readORwatched based on userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT ID FROM readORwatched WHERE userID = ? AND type = ?;"
    c.execute(command,(userID, "movie"))
    movies = c.fetchall()
    # print(books)
    db.close()
    list = []
    for id in movie:
        list.append(id[0])
    # print(list)
    return list

def get_books_wishlist(userID):
    '''gets books from wishlist based on userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT ID FROM wishlist WHERE userID = ? AND type = ?;"
    c.execute(command,(userID, "book"))
    books = c.fetchall()
    # print(books)
    db.close()
    list = []
    for id in books:
        list.append(id[0])
    # print(list)
    return list

def get_movies_wishlist(userID):
    '''gets movies from wishlist based on userID'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT ID FROM wishlist WHERE userID = ? AND type = ?;"
    c.execute(command,(userID, "movie"))
    movies = c.fetchall()
    # print(books)
    db.close()
    list = []
    for id in movies:
        list.append(id[0])
    # print(list)
    return list

def get_all_user_data():
    '''gets all user data into a dict'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command  = "SELECT username,password_hash FROM users;"
    c.execute(command)
    userInfo = c.fetchall()
    db.close()
    dict = {}
    for item in userInfo:
        dict[item[0]] = item[1]
    return dict


def get_user_id(username):
    '''gets user id based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id FROM users WHERE username = ?;"
    c.execute(command,(username,))
    user_id = c.fetchall()
    db.close()
    return user_id[0][0]


def get_username(id):
    '''get username based on id'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT username FROM users WHERE id = ?;"
    c.execute(command,(id,))
    name = c.fetchall()
    db.close()
    return name[0][0]
