# -*- coding: utf-8 -*-
"""sentiment analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jstLkNAuwDEblcd12A7AFA19dogiBqKh
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Step 1: Data Loader Class
class DataLoader:
    def __init__(self, num_words=10000, max_len=100):
        self.num_words = num_words
        self.max_len = max_len

    def load_data(self):
        imdb = tf.keras.datasets.imdb
        (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=self.num_words)
        return X_train, y_train, X_test, y_test

    def preprocess_data(self, X):
        return pad_sequences(X, maxlen=self.max_len)


# Demonstrating DataLoader class
data_loader = DataLoader()
X_train, y_train, X_test, y_test = data_loader.load_data()
X_train = data_loader.preprocess_data(X_train)
X_test = data_loader.preprocess_data(X_test)

print("DataLoader output:")
print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")
print(f"Example preprocessed sequence:\n{X_train[0]}")
print("\n" + "="*50 + "\n")

# Step 2: Model Builder Class
class SentimentRNN:
    def __init__(self, vocab_size, embedding_dim=128, rnn_units=64, dropout_rate=0.2):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.rnn_units = rnn_units
        self.dropout_rate = dropout_rate
        self.model = None

    def build_model(self):
        model = Sequential([
            Embedding(input_dim=self.vocab_size, output_dim=self.embedding_dim, input_length=100),
            LSTM(self.rnn_units, return_sequences=False),
            Dropout(self.dropout_rate),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model
        return model


# Demonstrating SentimentRNN class
model_builder = SentimentRNN(vocab_size=data_loader.num_words)
model = model_builder.build_model()
print("Model summary:")
model.summary()
print("\n" + "="*50 + "\n")

# Step 3: Training and Evaluation Class
class Trainer:
    def __init__(self, model, patience=3):
        self.model = model
        self.patience = patience
        self.history = None

    def train(self, X_train, y_train, X_val, y_val, batch_size=32, epochs=10):
        early_stopping = EarlyStopping(monitor='val_loss', patience=self.patience, restore_best_weights=True)
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=batch_size,
            epochs=epochs,
            callbacks=[early_stopping],
            verbose=1
        )

    def evaluate(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {loss:.4f}")
        print(f"Test Accuracy: {accuracy:.4f}")
        return loss, accuracy

    def plot_metrics(self):
        if self.history:
            plt.figure(figsize=(12, 5))
            plt.subplot(1, 2, 1)
            plt.plot(self.history.history['accuracy'], label='Training Accuracy')
            plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
            plt.legend()
            plt.title('Model Accuracy')

            plt.subplot(1, 2, 2)
            plt.plot(self.history.history['loss'], label='Training Loss')
            plt.plot(self.history.history['val_loss'], label='Validation Loss')
            plt.legend()
            plt.title('Model Loss')
            plt.show()
        else:
            print("No history to plot!")

# Splitting data for training and validation
X_val = X_train[:5000]
y_val = y_train[:5000]
X_train_main = X_train[5000:]
y_train_main = y_train[5000:]

# Demonstrating Trainer class
trainer = Trainer(model)
trainer.train(X_train_main, y_train_main, X_val, y_val)
trainer.evaluate(X_test, y_test)
trainer.plot_metrics()
print("\n" + "="*50 + "\n")


# Prediction and classification report
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix Plot
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# Evaluate the model on the test set
test_loss, test_accuracy = trainer.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

from sklearn.metrics import classification_report

# Generate predictions on the test set
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print("Classification Report:")
print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix
import seaborn as sns

# Create a confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# Define a function to decode reviews
word_index = tf.keras.datasets.imdb.get_word_index()
reverse_word_index = {value: key for (key, value) in word_index.items()}

def decode_review(text):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in text])

# Test on some random samples
for i in range(3):
    sample_index = np.random.randint(0, len(X_test))
    sample_review = X_test[sample_index]
    sample_label = y_test[sample_index]
    prediction = model.predict(np.array([sample_review]))[0][0]
    predicted_label = 1 if prediction > 0.5 else 0

    print(f"Sample Review (decoded): {decode_review(sample_review)}")
    print(f"True Label: {sample_label}, Predicted Label: {predicted_label}, Prediction Score: {prediction:.4f}")
    print("\n" + "="*50 + "\n")

import numpy as np

# Load the IMDb word index dictionary
word_index = imdb.get_word_index()
reverse_word_index = {value: key for (key, value) in word_index.items()}

def decode_review(encoded_review):
    """Decodes an integer-encoded review to human-readable text."""
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

# Select a few examples from the test set to demonstrate model predictions
for i in range(5):  # Show 5 sample reviews
    # Randomly choose a review from the test set
    sample_index = np.random.randint(0, len(X_test))
    sample_review = X_test[sample_index]
    true_label = y_test[sample_index]

    # Predict the sentiment
    prediction_score = model.predict(np.array([sample_review]))[0][0]
    predicted_label = 1 if prediction_score > 0.5 else 0

    # Decode the sample review
    decoded_review = decode_review(sample_review)

    # Display the results
    print(f"Sample Review {i + 1}:")
    print(f"Review Text:\n{decoded_review}")
    print(f"True Label: {'Positive' if true_label == 1 else 'Negative'}")
    print(f"Predicted Label: {'Positive' if predicted_label == 1 else 'Negative'}")
    print(f"Prediction Confidence: {prediction_score:.4f}")
    print("\n" + "="*80 + "\n")

import tensorflow as tf  # Import TensorFlow
import numpy as np

# Load the IMDb dataset and get the word index
imdb = tf.keras.datasets.imdb
word_index = imdb.get_word_index()
reverse_word_index = {value: key for (key, value) in word_index.items()}

def decode_review(encoded_review):
    """Decodes an integer-encoded review to human-readable text."""
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

# Select a few examples from the test set to demonstrate model predictions
for i in range(5):  # Show 5 sample reviews
    # Randomly choose a review from the test set
    sample_index = np.random.randint(0, len(X_test))
    sample_review = X_test[sample_index]
    true_label = y_test[sample_index]

    # Predict the sentiment
    prediction_score = model.predict(np.array([sample_review]))[0][0]
    predicted_label = 1 if prediction_score > 0.5 else 0

    # Decode the sample review
    decoded_review = decode_review(sample_review)

    # Display the results
    print(f"Sample Review {i + 1}:")
    print(f"Review Text:\n{decoded_review}")
    print(f"True Label: {'Positive' if true_label == 1 else 'Negative'}")
    print(f"Predicted Label: {'Positive' if predicted_label == 1 else 'Negative'}")
    print(f"Prediction Confidence: {prediction_score:.4f}")
    print("\n" + "="*80 + "\n")

import tensorflow as tf
import numpy as np

# Example unseen review
unseen_review = "I didnt like the movie! It was absolutely boring."

# Step 1: Preprocess the unseen review
# Tokenizing the review (convert words to indices based on the IMDB dataset's word index)
def preprocess_review(review, max_len=100):
    # Convert words to lower case and tokenize the review into integers
    word_index = imdb.get_word_index()
    # Add 3 to account for special tokens: 0: padding, 1: start of sequence, 2: unknown word
    encoded_review = [word_index.get(word, 2) for word in review.lower().split()]
    # Pad the sequence to ensure it has the same length as the model expects (100 tokens)
    return tf.keras.preprocessing.sequence.pad_sequences([encoded_review], maxlen=max_len)

preprocessed_review = preprocess_review(unseen_review)

# Step 2: Make prediction on the unseen review
prediction_score = model.predict(preprocessed_review)[0][0]
predicted_label = 1 if prediction_score > 0.5 else 0

# Step 3: Interpret the result
print(f"Unseen Review: {unseen_review}")
print(f"Prediction Confidence: {prediction_score:.4f}")
print(f"Predicted Label: {'Positive' if predicted_label == 1 else 'Negative'}")