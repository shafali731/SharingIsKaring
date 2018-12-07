import sqlite3

'''Creates the database with three tables: users, wishlist, and readORWatched.'''
db = sqlite3.connect("../data/database.db")
c = db.cursor()
#create users
command = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password_hash TEXT)"
c.execute(command)

command = "CREATE TABLE wishlist(userID INTEGER, ID TEXT, type TEXT)"
c.execute(command)

command = "CREATE TABLE readORwatched(userID INTEGER, ID TEXT, type TEXT)"
c.execute(command)

db.commit()
db.close()
