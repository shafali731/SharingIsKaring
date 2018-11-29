from flask import Flask, request, render_template, session, redirect, flash
import util.accounts
import util.posts
import util.sessions
import util.search

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    util.posts.create_table()
    util.accounts.create_table()
    app.debug = True  # Set to `False` before release
    app.run()
