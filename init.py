from flask import Flask, render_template, request, jsonify
from chatbot import intents_en, intents_ar
from chatbot import match_intent, check_exit, generate_response

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    lang = request.form['lang']
    if check_exit(user_input):
        response = "Goodbye!" if lang == 'en' else "وداعًا!"
    else:
        intent = match_intent(user_input, lang)
        response = generate_response(intent, lang) if intent else "Sorry, I didn't understand your question."
    return response

@app.route('/intents')
def get_intents():
    global intents_en, intents_ar  # Access global variables
    intents_en_list = [intent_data['queries'][0] for intent_data in intents_en.values()]
    intents_ar_list = [intent_data['queries'][0] for intent_data in intents_ar.values()]
    return jsonify({"intents_en": intents_en_list, "intents_ar": intents_ar_list})

if __name__ == '__main__':
    app.run(debug=True)
