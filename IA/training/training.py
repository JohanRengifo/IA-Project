import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.models import load_model
from sklearn.preprocessing import LabelBinarizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Load existing data
intents = json.load(open('../conversations/intents.json', encoding='utf-8'))

# Try to load the existing model
try:
    model = load_model('../models/chatbot_model.h5')
    print("Model loaded successfully.")
except (OSError, IOError, ValueError):
    print("No existing model found. Creating a new model.")

# Data preprocessing
lemmatizer = WordNetLemmatizer()
words = []
classes = []
documents = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern.lower())
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Process words and remove duplicates
words = sorted(set([lemmatizer.lemmatize(word) for word in words]))

# Create the updated training matrix
X = []  # Features
y = []  # Labels

output_empty = [0] * len(classes)
max_len = len(words)

for document in documents:
    bag = [0] * max_len  # Initialize with zeros
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word) for word in word_patterns]

    for word in words:
        if word in word_patterns:
            bag[words.index(word)] = 1

    X.append(bag)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    y.append(output_row)

# Convert features and labels to NumPy arrays
X = np.array(X)
y = np.array(y)

# Create and train the model (updated)
model = Sequential()
model.add(Dense(128, input_dim=len(X[0]), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y[0]), activation='softmax'))

# Compile the model with the Keras SGD optimizer
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=200, batch_size=5, verbose=1)

# Save the updated model
model.save('../models/chatbot_model.h5')
print("Model trained and saved.")