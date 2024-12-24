from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/')
def index():
    return render_template('landing.html')



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user = db.session.query(User).first()

    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages)

    intent = request.form.get('intent')

    intents = {
        'Quiero tener suerte': 'Recomiéndame una película',
        'Terror': 'Recomiéndame una película de terror',
        'Acción': 'Recomiéndame una película de acción',
        'Comedia': 'Recomiéndame una película de comedia',
        'Enviar': request.form.get('message')
    }

    if intent in intents:
        user_message = intents[intent]

        # Guardar nuevo mensaje en la BD
        db.session.add(Message(content=user_message, author="user", user=user))
        db.session.commit()

        messages_for_llm = [{
            "role": "system",
            "content": "Eres un chatbot que recomienda películas, te llamas 'Questy'. Tu rol es ser un experto cineasta encargado de responder recomendaciones específicas de manera concisa sobre consultas. Ayudas a usuarios que son cinéfilos y desean ir más allá de lo comercial. No repitas recomendaciones.",
        }]

        for message in user.messages:
            messages_for_llm.append({
                "role": message.author,
                "content": message.content,
            })

        chat_completion = client.chat.completions.create(
            messages=messages_for_llm,
            model="gpt-4o",
            temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        db.session.add(Message(content=model_recommendation, author="assistant", user=user))
        db.session.commit()

        return render_template('chat.html', messages=user.messages)


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
    user = db.session.query(User).first()
    data = request.get_json()
    user_message = data['message']
    new_message = Message(content=user_message, author="user", user=user)
    db.session.add(new_message)
    db.session.commit()

    messages_for_llm = [{
        "role": "system",
        "content": "Eres MovieQuest, un chatbot experto en cine, creado para recomendar películas a cinéfilos y profesionales del cine. Debes proporcionar recomendaciones de manera breve, concisa y especializada, sin repetir nunca las sugerencias. Asegúrate de ofrecer respuestas ajustadas al nivel de conocimiento del usuario, manteniendo la relevancia y la precisión en cada recomendación.",
    }]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }
