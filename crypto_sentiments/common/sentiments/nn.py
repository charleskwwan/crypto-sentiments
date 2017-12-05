import os


from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

EMBEDDING_DIM = 25
MAX_SEQUENCE_LENGTH = 1000
MAX_NB_WORDS = 20000

def tokenize_incoming_data(X_raw):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(X_raw)
    sequences = tokenizer.texts_to_sequences(X_raw)
    word_index = tokenizer.word_index
    X_processed = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    return X_processed, word_index


class TweetNeuralNetwork: 

    def __init__(self): 
        self.model = None


    def load(self, filename, filename_weights): 
        self.model = load_model(filename)
        self.model.load_weights(filename_weights)


    def classify(self, tweet):
        X, word_index = tokenize_incoming_data([tweet])

        predictions = self.model.predict(x=X, batch_size=128)
        is_positive = predictions[0][1] >= 0.5
        
        sentiment = "positive" if is_positive else "negative"
        return sentiment


if __name__ == '__main__':
    classifier = TweetNeuralNetwork()

    classifier_file = os.getcwd() + '/model/classifier.h5'
    weights_file = os.getcwd() + '/model/weightsV2.h5'
    classifier.load(classifier_file, weights_file)

    while(True): 
        text = input("Type in a Tweet for Sentiment: ")
        if (text == "quit"): 
            break
        print(classifier.classify(text))

    


            










