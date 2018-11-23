from flask import Flask, request, render_template, session, redirect, flash

app = Flask(__name__)

#OMDb apikey=1891fe35

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html', error=False)

@app.route('/signup')
def signup():
    return render_template('signup.html', error=False)

@app.route('/book_info/<bookID>')
def book(book):
    return render_template('book_info.html')

@app.route('/movie_info/<movieID>')
def movie(movie):
    return render_template('movie_info.html')


if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()
