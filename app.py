from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
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
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Quiero ver una película de terror, ¿cuál me recomiendas?",
            }
        ],
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }
