import csv
from flask import Flask, jsonify, request
# importing files

from demographicFiltering import output
from contentBasedFiltering import get_recommendations

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
    articles_data = {
        # url == 11
        # title == 12
        # text == 13
        # language == 14
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
    }
    return jsonify({"data": articles_data, "status": 200})


@app.route("/liked_articles", methods=["POST"])
def liked_articles():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)

    return jsonify({"liked_articles_data": liked_articles, "status": 200})


@app.route('/non_liked_articles', methods=["POST"])
def non_liked_articles():
    article = all_articles[0]
    non_liked_articles.append(article)
    all_articles.pop(0)

    return jsonify({"non_liked_articles": non_liked_articles, "status": 200})


@app.route("/recommended_articles")
def recommended_articles():
    all_recommended_articles = []
    for each_liked_article in liked_articles:
        output = get_recommendations(each_liked_article[4])
        for data in output:
            all_recommended_articles.append(data)
    import itertools
    all_recommended_articles.sort()
    all_recommended_articles = list(all_recommended_articles for all_recommended_articles,
                                    _ in itertools.groupby(all_recommended_articles))
    article_data = []
    for each_article in all_recommended_articles:
        obj_data = {
            "url": each_article[0],
            "title": each_article[1],
            "text": each_article[2],
            "lang": each_article[3],
        }
        article_data.append(obj_data)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)

# gg 