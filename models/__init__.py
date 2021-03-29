import os
import pickle
from string import punctuation

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn import svm
from sklearn.model_selection import train_test_split

from .category import Category, SUBCATEGORIES
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
        if word not in punctuation and word.lower() not in stopwords_
    ]

    return " ".join(optimized_words)


def predict(nlp, model, x):
    docs = [nlp(optimized_phrase(text)) for text in x]
    word_vectors = [x.vector for x in docs]
    return model.predict(word_vectors)[0]


def dump(model, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(model, f)


def load(file_path):
    with open(file_path, "rb") as f:
        model = pickle.load(f)

    return model


def train(dataframe):
    nlp = load_nlp()
    docs = [nlp(optimized_phrase(text)) for text in dataframe["text"]]
    word_vectors = [x.vector for x in docs]

    X_train, X_test, y_train, y_test = train_test_split(
        word_vectors, dataframe["category"], test_size=0.35
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

    categories = Category.values()
    category_df = load_df(
        categories, os.getenv("CATEGORY_DATAFRAME_FILE_PATH")
    )
    category_model = train(category_df)

    frontend_subcategories = [
        c.value for c in SUBCATEGORIES[Category.FRONTEND]
    ]
    frontend_df = load_df(
        frontend_subcategories,
        os.getenv("FRONTEND_SUBCATEGORY_DATAFRAME_FILE_PATH"),
    )
    frontend_model = train(frontend_df)

    backend_subcategories = [c.value for c in SUBCATEGORIES[Category.BACKEND]]
    backend_df = load_df(
        backend_subcategories,
        os.getenv("BACKEND_SUBCATEGORY_DATAFRAME_FILE_PATH"),
    )
    backend_model = train(backend_df)

    dump(category_model, os.getenv("CATEGORY_MODEL_FILE_PATH"))
    dump(frontend_model, os.getenv("FRONTEND_SUBCATEGORY_MODEL_FILE_PATH"))
    dump(backend_model, os.getenv("BACKEND_SUBCATEGORY_MODEL_FILE_PATH"))
