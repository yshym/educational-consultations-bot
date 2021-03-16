import pickle

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn import svm
from sklearn.model_selection import train_test_split

from .data import load_df


def load_nlp():
    return spacy.load("en_core_web_lg")


def optimized_phrase(phrase):
    stopwords_ = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()

    words = word_tokenize(phrase)
    optimized_words = [
        lemmatizer.lemmatize(word.lower())
        for word in words
        if word.isalpha() and word.lower() not in stopwords_
    ]

    return " ".join(optimized_words)


def predict(nlp, model, x):
    docs = [nlp(optimized_phrase(text)) for text in x]
    word_vectors = [x.vector for x in docs]
    return model.predict(word_vectors)[0]


def dump(model):
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)


def load():
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)

    return model


def train():
    nlp = load_nlp()
    df = load_df()
    docs = [nlp(optimized_phrase(text)) for text in df["text"]]
    word_vectors = [x.vector for x in docs]

    X_train, X_test, y_train, y_test = train_test_split(
        word_vectors, df["category"], test_size=0.35
    )

    model = svm.SVC(kernel="linear")
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model score: {score}")

    return model


def init():
    nltk.download("wordnet")
    nltk.download("stopwords")
    nltk.download("punkt")

    model = train()
    dump(model)
