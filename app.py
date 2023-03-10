from flask import Flask, render_template, request
import openai
import random
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm good, thank you!", "I'm doing well, how about you?", "I'm great, thanks for asking!"],
    "bye": ["Goodbye!", "See you later!", "Bye!"]
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.get_json()['user_input']
    if user_input.lower() == "bye":
        bot_response = respond("bye")
    else:
        bot_response = respond(user_input)
        bot_response = bot_response.replace('\n', '<br/>')
    return bot_response


def respond(text):
    for key in responses:
        if text.lower() == key:
            return random.choice(responses[key])
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"].strip()


if __name__ == '__main__':
    app.run()
