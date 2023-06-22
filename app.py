from time import sleep

from flask import Flask, render_template, request, jsonify
import openai

from chat_bot import get_answer
from translate import to_en

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/send-message', methods=['POST'])
def sendMessage():
    data = request.get_json()
    message = data.get('message')
    if message:
        return get_answer(to_en(message))
    else:
        return 'ცარიელ ტექსტს ნუ გზავნი ჩემო ძმაო !'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
