import os
import pickle

from bs4 import BeautifulSoup
from pandas_gbq import read_gbq

from .category import Category


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
    WHERE {category_conditions(Category.values())}
    LIMIT 10000
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
    df["category"] = df.apply(category(Category.values()), axis=1)
    df = df.drop(columns=["title", "body", "tags"])

    return df
