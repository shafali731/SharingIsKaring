import sqlite3

db = sqlite3.connect("../data/database.db")
c = db.cursor()
#create users
command = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password_hash TEXT)"
c.execute(command)
#create contributions
command = "CREATE TABLE book(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,author TEXT, ISBN TEXT, genre TEXT)"
c.execute(command)
#create stories
command = "CREATE TABLE movie(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, genre TEXT)"
c.execute(command)

command = "CREATE TABLE wishlist(userID INTEGER, title TEXT, type TEXT)"
c.execute(command)

command = "CREATE TABLE readORwatched(userID INTEGER, title TEXT, type TEXT)"
c.execute(command)

db.commit()
db.close()
