import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Inicialización de WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Cargamos los archivos generados previamente
with open('./conversations/intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)
with open('../models/words.pkl', 'rb') as file:
    words = pickle.load(file)
with open('../models/classes.pkl', 'rb') as file:
    classes = pickle.load(file)

# Cargamos el modelo
model = load_model('../models/chatbot_model.h5')

# Función para limpiar una oración
def clean_up_sentence(sentence):
    """
    Limpia una oración tokenizando y lematizando las palabras.

    :param sentence: La oración que se va a limpiar.
    :return: Una lista de palabras lematizadas.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Función para convertir la oración en una bolsa de palabras
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Función para predecir la categoría de una oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.argmax(res)
    category = classes[max_index]
    return category

# Función para obtener una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Bucle principal del chat
print("Asistente en Funcionamiento")
print("Por favor, realiza preguntas específicas para obtener respuestas adecuadas.")
print("Escribe 'salir' para finalizar el Asistente.")
print("β - version")

while True:
    message = input("Tú: ")
    if message.lower() == 'salir':
        break
    intent = predict_class(message)
    response = get_response(intent, intents)
    print("Chatbot:", response)
