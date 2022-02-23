from crypt import methods
import csv
from flask import Flask, jsonify, request
from tqdm import main


all_articles = []

with open("articles.csv") as f:
    # reading the csv and storing it in Reader variable
    Reader = csv.reader(f)

    # converting the readed csv into a list (array)
    data = list(Reader)

    # excluding the main header from the array variable
    all_articles = data[1:]


liked_articles = []
non_liked_articles = []

app = Flask(__name__)


@app.route("/")
def getArticles():
    return jsonify({"data": all_articles[0], "status": 200})


@app.route("/liked_articles", methods=["POST"])
def liked_articles():
    article = all_articles[0]
    all_articles = all_articles[1]
    liked_articles.append(article)

    return jsonify({"liked_articles_data": liked_articles, "status": 200})


@app.route('/non_liked_articles', methods=["POST"])
def non_liked_articles():
    article = all_articles[0]
    all_articles = all_articles[1]
    non_liked_articles.append(article)

    return jsonify({"non_liked_articles": non_liked_articles, "status": 200})


if __name__ == '__main__':
    app.run(debug=True)
