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
