# -*- coding: utf-8 -*-
"""text_class.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cPWZjiT7LtVys1hbAVNymRqB9Y0aFV-Z
"""

import numpy as np
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import seaborn as sbn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
# %matplotlib inline

## load dataset
df = pd.read_csv("bbc-text.csv")
df.head(10)

df.shape

df['text'][0]

df['category'].unique()

df['category'].value_counts()

sbn.countplot(df['category'])

# Use sklearn utility to convert label strings to numbered index
from sklearn.preprocessing import LabelEncoder
df["category"] = LabelEncoder().fit_transform(df["category"])
df.head()

#tokenize the words (text)
stemmer = PorterStemmer()
words = stopwords.words("english")
df['text'] = df['text'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
final_features = vectorizer.fit_transform(df['text']).toarray()
df.head()

#split the data into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], test_size=0.30, random_state=0)
# Inspect the dimenstions of our training and test data
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#convert to a vector with 1000 words
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features = 1000)
vectorizer.fit(X_train)

X_train = vectorizer.transform(X_train)
X_test  = vectorizer.transform(X_test)
X_train = X_train.todense()

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

print("Accuracy of Logistic Regression:", score)

# Converts the labels to a one-hot representation
import keras
num_classes = np.max(y_train) + 1
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Build the model
from tensorflow import keras
layers = keras.layers
models = keras.models
from keras.models import Sequential
from keras.layers import Dense
model = Sequential()

model.add(Dense(20, input_dim= 1000,activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(num_classes , activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

history = model.fit(X_train, y_train,
                    epochs=50,
                    validation_split=0.10,
                     batch_size=4)

loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

def plot_history(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training acc')
    plt.plot(x, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

plot_history(history)

y_softmax = model.predict(X_test)

y_test_1d = []
y_pred_1d = []

for i in range(len(y_test)):
    probs = y_test[i]
    index_arr = np.nonzero(probs)
    one_hot_index = index_arr[0].item(0)
    y_test_1d.append(one_hot_index)

for i in range(0, len(y_softmax)):
    probs = y_softmax[i]
    predicted_index = np.argmax(probs)
    y_pred_1d.append(predicted_index)

from sklearn import metrics

print(metrics.confusion_matrix(y_test_1d, y_pred_1d))

print(metrics.classification_report(y_test_1d, y_pred_1d))

from sklearn.metrics import accuracy_score

print("Accuracy of Deep Model is:",accuracy_score(y_test_1d, y_pred_1d))

