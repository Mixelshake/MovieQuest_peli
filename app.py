from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/user/<username>')
def user(username):
    favorite_movies = [
        'The Shawshank Redemption',
        'The Godfather',
        'The Dark Knight',
    ]
    return render_template('user.html', username=username, favorite_movies=favorite_movies)
