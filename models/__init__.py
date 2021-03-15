import os
import pickle

import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pandas_gbq import read_gbq
from sklearn import svm
from sklearn.model_selection import train_test_split


def load_nlp():
    return spacy.load("en_core_web_lg")


def fetch_questions_query():
    def category_conditions(categories):
        conditions = ""

        for c in categories:
            if conditions:
                conditions += "\n\tOR "

            positive_conditions = f"""(tags LIKE '%|{c}|%'
            OR tags LIKE '%|{c}'
            OR tags LIKE '{c}|%'
            OR tags LIKE '{c}')"""
            negative_conditions = " AND ".join(
                f"""(tags NOT LIKE '%|{oc}|%'
                AND tags NOT LIKE '%|{oc}%'
                AND tags NOT LIKE '%{oc}|%')"""
                for oc in [x for x in categories if x != c]
            )
            conditions += (
                f"{positive_conditions}\n\t\tAND {negative_conditions}"
            )

        return conditions

    query = f"""
    SELECT title, body, tags
    FROM `bigquery-public-data.stackoverflow.posts_questions`
    WHERE {category_conditions(['frontend', 'backend'])}
    LIMIT 5000
    """

    return query


def category(categories):
    def f(row):
        for c in categories:
            if c in row["tags"]:
                value = c
                break

        return value

    return f


def load_df():
    df_file = "models/df.pkl"

    if os.path.isfile(df_file):
        with open(df_file, "rb") as f:
            df = pickle.load(f)
    else:
        query = fetch_questions_query()
        df = read_gbq(query, project_id=os.getenv("GOOGLE_PROJECT_ID"))
        with open(df_file, "wb") as f:
            pickle.dump(df, f)

    df["text"] = df["title"] + [
        BeautifulSoup(body, "html.parser").get_text() for body in df["body"]
    ]
    df["category"] = df.apply(category(["frontend", "backend"]), axis=1)
    df = df.drop(columns=["title", "body", "tags"])

    return df


def lemmatized_phrase(phrase):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(phrase)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)


def predict(nlp, model, x):
    docs = [nlp(lemmatized_phrase(text)) for text in x]
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
    docs = [nlp(lemmatized_phrase(text)) for text in df["text"]]
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
