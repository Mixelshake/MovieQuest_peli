from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/')
def index():
    return render_template('landing.html')


messages = [
    {
        "role": "system",
        "content": "Eres un chatbot que recomienda películas, te llamas 'Next Moby'. Tu rol es responder recomendaciones de manera breve y concisa. No repitas recomendaciones.",
    }
]


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')

    intent = request.form.get('intent')

    intents = {
        'Quiero tener suerte': 'Recomiéndame una película',
        'Terror': 'Recomiéndame una película de terror',
        'Acción': 'Recomiéndame una película de acción',
        'Comedia': 'Recomiéndame una película de comedia',
    }

    if intent in intents:
        user_message = intents[intent]

        messages.append({
            "role": "user",
            "content": user_message,
        })

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        messages.append({
            "role": "assistant",
            "content": model_recommendation,
        })

        return render_template('chat.html', recommendation=model_recommendation)


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
    data = request.get_json()
    user_message = data['message']
    messages.append({
        "role": "user",
        "content": user_message,
    })

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }
