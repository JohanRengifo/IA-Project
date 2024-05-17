import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, jsonify

# Inicialización de Flask
app = Flask(__name__)

# Configuración de codificación UTF-8
app.config['JSON_AS_ASCII'] = False

# Cargar datos y modelos previos
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')

intents = json.loads(open('../../training/conversations/intents.json').read())
words = pickle.load(open('../../models/words.pkl', 'rb'))
classes = pickle.load(open('../../models/classes.pkl', 'rb'))
model = load_model('../../models/chatbot_model.h5')

# Función para determinar la intención del usuario
def determinar_intencion_del_usuario(user_message):
    # Procesar el mensaje del usuario de la misma manera que en el entrenamiento
    sentence_words = nltk.word_tokenize(user_message.lower())
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

    # Crear una bolsa de palabras (bag of words) para la entrada del modelo
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    # Realizar la predicción de la intención
    res = model.predict(np.array([bag]))[0]
    max_index = np.argmax(res)
    predicted_intent = classes[max_index]

    return predicted_intent

# Función para obtener una respuesta del chatbot
def obtener_respuesta_del_chatbot(user_message):
    intencion_detectada = determinar_intencion_del_usuario(user_message)

    # Lógica para obtener una respuesta del chatbot basada en la intención
    if intencion_detectada == "saludar":
        respuesta = "Hola, ¿en qué puedo ayudarte?"
    elif intencion_detectada == "despedida":
        respuesta = "Adiós, ha sido un placer hablar contigo."
    elif intencion_detectada == "pregunta":
        respuesta = responder_pregunta(user_message)
    else:
        respuesta = "Lo siento, no entiendo tu pregunta."

    return respuesta

# Función para responder a preguntas
def responder_pregunta(pregunta):
    # Intenta encontrar una respuesta en el modelo de lenguaje
    respuesta_modelo = model.predict(pregunta)
    if respuesta_modelo:
        return respuesta_modelo[0][0]

#Respuesta Manueal
def get_respuesta_manual(pregunta):
    # Lógica para obtener una respuesta manual
    respuesta = "Esta es una respuesta manual para la pregunta: " + pregunta
    return respuesta

# Rutas de Flask
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')  # Obtiene el campo 'message' del JSON
    bot_response = obtener_respuesta_del_chatbot(user_message)
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)