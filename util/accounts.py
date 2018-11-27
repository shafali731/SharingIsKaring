from flask import Flask, request, render_template, session, redirect, flash, url_for
from passlib.hash import md5_crypt

from util import dbcommands as db

def is_logged_in():
    '''This checks if the user is logged in.'''
    return "id" in session

def loginAuthentication():
    user_data = db.get_all_user_data() #for updating user_data when there is a new user
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    #Checks if user/pass is valid if not flash reasons why
    if username_input in user_data:
        #verifies the hashed password with given password
        if md5_crypt.verify(password_input, user_data[username_input]):
            id = db.get_user_id(username_input)
            session["id"] = id
        else:
            flash("Invalid password, try again!")
            return redirect(url_for('login'))
    else:
        flash("Invalid username, try again!")
        return redirect(url_for('login'))
    return redirect(url_for('index'))

def signupAuthentication():
    user_data = db.get_all_user_data()
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    password_input2 = request.form.get("password2")
    #checks if there is an user with the same username
    if username_input in user_data:
        flash("Username already exists! Please pick another one!")
        return redirect(url_for("signup"))
    #checks if the user typed the same passward twice
    elif len(username_input) < 4:
        flash("Username has to be at least 4 characters!")
        return redirect(url_for("signup"))
    elif password_input != password_input2:
        flash("Input Same Password in Both Fields!")
        return redirect(url_for("signup"))
    else:
        #adds the user's username and a hashed + salted
        #version of his password to database
        db.add_user(username_input, md5_crypt.encrypt(password_input))
        flash("Successfully Registered, Now Sign In!")
        return render_template('login.html', success=True)
