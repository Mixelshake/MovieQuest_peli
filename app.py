from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

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

@app.post('/recommend')
def recommend():
    return {
        'recommendation': 'Te recomiendo ver Star Wars',
        'other': [
            'The Shawshank Redemption',
            'The Godfather',
            'The Dark Knight',
        ]
    }
