import numpy as np
import pickle
from typing import Tuple
import matplotlib.pyplot as plt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam


SPLITTER: str = ';'  # comes from tokenizer


def load_tokenizer(tokenizer_path: str):
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer


def prepare_data(tokenizer: Tokenizer, texts: list[str], input_seq_x_len: int = 3) -> Tuple[np.ndarray, np.ndarray]:  
    # shapes of output: (:, input_seq_x_len), (:, 1)
    total_words = len(tokenizer.word_index) + 1
    input_sequences = []

    for text in tqdm(texts):
        token_list = tokenizer.texts_to_sequences([text])[0]
        for i in range(len(token_list)):
            input_sequences.append(token_list[max(0, i-input_seq_x_len):i+1])

    input_sequences = pad_sequences(input_sequences, maxlen=input_seq_x_len + 1, padding='pre')
    X, y = input_sequences[:, :-1], input_sequences[:, -1]
    return X, y, total_words


def build_model(total_words: int, embedding_size: int = 100, input_seq_x_len: int = 3) -> Model:
    model = Sequential()
    model.add(Embedding(total_words, embedding_size, input_length=input_seq_x_len))
    model.add(LSTM(100))
    model.add(Dropout(0.2))
    model.add(Dense(total_words, activation='softmax'))
    return model


def train(model, X: np.ndarray, y: np.ndarray, epochs: int = 100, learning_rate: float = 0.01, validation_split: float = 0.2, model_filepath: str = 'model.keras') -> None:
    model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=learning_rate), metrics=['accuracy'])
    history = model.fit(X, y, epochs=epochs, verbose=1, validation_split=validation_split)

    def plot_history(history, metric, ylabel, filename):
        plt.plot(history.history[metric], label=metric)
        plt.plot(history.history[f'val_{metric}'], label=f'val_{metric}')
        plt.xlabel('Epoch')
        plt.ylabel(ylabel)
        plt.legend(loc='lower right' if metric == 'accuracy' else 'upper right')
        plt.savefig(filename)
        plt.show()

    plot_history(history, 'accuracy', 'Accuracy', 'accuracy.png')
    plot_history(history, 'loss', 'Loss', 'loss.png')

    model.save(model_filepath)
    print("Model Saved")


def create_prediction_mask(tokenizer: Tokenizer, words_whitelist: list[str]) -> np.ndarray: 
    mask = np.zeros(len(tokenizer.word_index) + 1, dtype=bool)
    for word in words_whitelist:
        token = tokenizer.word_index.get(word)
        if token is not None:
            mask[token] = True
    return mask


def predict_next_word(tokenizer: Tokenizer, model: Model, input_text: str, mask: np.ndarray|None = None, input_seq_x_len: int = 3, top_n: int = 1) -> list:
    token_list = tokenizer.texts_to_sequences([input_text])[0]
    token_list = pad_sequences([token_list], maxlen=input_seq_x_len, padding='pre')
    predicted = model.predict(token_list, verbose=0)[0]

    if mask is not None:
        masked_predictions = np.ma.array(predicted, mask=~mask)
        sorted_indices = masked_predictions.argsort()[::-1]
        valid_indices = [idx for idx in sorted_indices if not masked_predictions.mask[idx]]
        predicted_indices = valid_indices[:top_n]
        predicted_probs = masked_predictions[predicted_indices].data
    else:
        sorted_indices = predicted.argsort()[::-1]
        predicted_indices = sorted_indices[:top_n]
        predicted_probs = predicted[predicted_indices]

    output_words = [(tokenizer.index_word.get(i), prob) for i, prob in zip(predicted_indices, predicted_probs) if i in tokenizer.index_word]
    return output_words[0][0]  # returning top-one word, todo: add extra processing logic


if __name__ == '__main__':
    tokenizer = load_tokenizer('./models/tokenizer.pkl')
    model = load_model('./models/model.h5')
    print(predict_next_word(tokenizer, model, "молоко"))