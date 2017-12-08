from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Input,  Flatten
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D, Embedding

from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix

import os
import csv
import numpy as np
from numpy.random import RandomState

from crypto_sentiments.common.scrape import prune_tweet

TRAIN_DATA_CORPUS = './crypto_sentiments/data/nn/twitter_corpus.csv'
GLOVE_EMBEDDINGS = './crypto_sentiments/data/nn/glove.twitter.27B.25d.txt'

EMBEDDING_DIM = 25
MAX_SEQUENCE_LENGTH = 1000
MAX_NB_WORDS = 20000

PERCENT_VALIDATION = 0.2

PERCENT_DATASET = 0.5

random = RandomState(3)

def main():

    labels_index = { 'Negative': 0, 'Positive': 1}
    word_index, x_train, x_val, y_train, y_val = get_training_and_validation_sets()

    model = make_model(labels_index, word_index)
    train(model, x_train, x_val, y_train, y_val)

    valid_predicted_out = model.predict(x=x_val, batch_size=256)
    evaluate(y_val, valid_predicted_out)


def load_data_set():
    X = []
    Y = []

    with open(TRAIN_DATA_CORPUS, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = row['\ufeffItemID']
            tweet_text = row['SentimentText']
            label =  int(row['Sentiment'])

            X.append(tweet_text)
            Y.append(label) 

    return X[:300000],Y[:300000]


def tokenize_data(X_raw, Y_raw):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(X_raw)
    sequences = tokenizer.texts_to_sequences(X_raw)
    word_index = tokenizer.word_index
    X_processed = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    Y_processed = to_categorical(np.asarray(Y_raw), 2)

    return X_processed, Y_processed, word_index


def tokenize_incoming_data(X_raw):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(X_raw)
    sequences = tokenizer.texts_to_sequences(X_raw)
    word_index = tokenizer.word_index
    X_processed = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    return X_processed, word_index


def split_the_data(X_processed, Y_processed):
    indices = np.arange(X_processed.shape[0])
    random.shuffle(indices)
    x_shuffled = X_processed[indices]
    y_shuffled = Y_processed[indices]

    num_validation_samples = int(PERCENT_VALIDATION * x_shuffled.shape[0])
    
    x_train = x_shuffled[:-num_validation_samples]
    y_train = y_shuffled[:-num_validation_samples]
    
    x_val = x_shuffled[-num_validation_samples:]
    y_val = y_shuffled[-num_validation_samples:]

    return x_train, x_val, y_train, y_val


def get_training_and_validation_sets():
    print('loading data')
    X_raw, Y_raw = load_data_set()
    X_pruned_raw = [prune_tweet(row) for row in X_raw]

    print('tokenizing data')
    X_processed, Y_processed, word_index = tokenize_data(X_pruned_raw, Y_raw)
    x_train, x_val, y_train, y_val = split_the_data(X_processed, Y_processed)

    return word_index, x_train, x_val, y_train, y_val


def get_embeddings():
    embeddings = {}
    with open(GLOVE_EMBEDDINGS, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings[word] = coefs
    return embeddings
    

def make_embedding_layer(word_index):
    embeddings = get_embeddings()
    num_unique_words = len(word_index)
    nb_words = min(MAX_NB_WORDS, len(word_index))
    embedding_matrix = np.zeros((nb_words, EMBEDDING_DIM))

    for word, i in word_index.items():
        if i >= MAX_NB_WORDS or i >= num_unique_words:
            continue
        embedding_vector = embeddings.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    embedding_layer = Embedding(nb_words, EMBEDDING_DIM, weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH, trainable=False)
    return embedding_layer


def make_model(labels_index, word_index):
    embedded_sequences = make_embedding_layer(word_index)
    
    model = Sequential([
        embedded_sequences,
        Conv1D(512, 5, activation='relu'),
        AveragePooling1D(5),
        Conv1D(256, 5, activation='relu'),
        AveragePooling1D(5),
        Conv1D(128, 5, activation='relu'),
        MaxPooling1D(5),
        Flatten(),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dense(len(labels_index), activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
    return model


def train(model, x_train, x_val, y_train, y_val):
    print("Train")
    cb = [ModelCheckpoint(os.getcwd() + "./../models/weights_new.h5", save_best_only=True, save_weights_only=False)]
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=2, batch_size=256, callbacks=cb)
    model.save(os.getcwd() + "./../models/model_new.h5")


def evaluate(expected_out, predicted_out):
    expected_categories = [np.argmax(x) for x in expected_out]
    predicted_categories = [np.argmax(x) for x in predicted_out]
    cm = confusion_matrix(expected_categories, predicted_categories)
    print(cm)


def run_model_unseen(): 

    X_raw = ["school is fun",
             "I love my best friend", 
             "That steak was good", 
             "bitcoin just reached 10 thousand dollars", 
             "cryptocurrency is the disrupting the future",
             "Bitcoin just lost 5000 dollars, it's going bankrupt", 
             "banks ban bitcoin from entering the market", 
             "The stocks are falling", 
             "The bubble is going to pop", 
             "The Queen's bank, Coutts, has no plans to invest in bitcoin because it is backed by nothing but sentiment"]

    X, word_index = tokenize_incoming_data(X_raw)

    model = load_model(os.getcwd() + '/model/model3.h5')
    model.load_weights(os.getcwd() + '/model/weights3.h5')

    predictions = model.predict(x=X, batch_size=128)

    for index, txt in enumerate(X_raw):
        is_positive = predictions[index][1] >= 0.5
        status_txt = "Positive" if is_positive else "Negative"
        print("[",status_txt,"] ", txt)



if __name__ == '__main__':
    main()
    # run_model_unseen()