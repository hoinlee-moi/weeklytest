from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail/<idx>')
def detail(idx):
    article = db.test.find_one({'idx': int(idx)}, {'_id': False})

    return render_template("detail.html", article=article)
    # todo

@app.route('/articleList', methods=['GET'])
def get_article_list():
    order = request.args.get('order')
    if order == "desc":
        article_list = list(db.homework.find({}, {'_id': False}).sort([("read_count", -1)]))
    else:
        article_list = list(db.homework.find({}, {'_id': False}).sort([("read_count", 1)]))

    for article in article_list:
        article['date'] = article['date'].strftime('%Y.%m.%d %H:%M:%S')

    return jsonify({"article_list": article_list})

# Create
@app.route('/article', methods=['POST'])
def create_article():
    # todo
    if 0 >= db.homework.estimated_document_count():
        idx = 1
    else:
        idx = list(db.homework.find({}, sort=[('_id', -1)]).limit(1))[0]['idx'] + 1


    title_give = request.form['title']
    content_give = request.form['content']
    pw_give = request.form['pw']



    doc={
        'idx': idx,
        'title':title_give,
        'content':content_give,
        'pw': pw_give,
        'date':datetime.now(),
        'read_count': 0
    }

    db.homework.insert_one(doc)
    return {"result": "success"}

# Read
@app.route('/article', methods=['GET'])
def read_article():
    idx = request.args['idx']
    db.article.update_one({'idx':int(idx)}, {'$inc': {'read_count':1}})
    return jsonify({"article": article})

# Update
@app.route('/article', methods=['PUT'])
def update_article():
    idx = request.form.get('idx')
    title = request.form.get('title')
    content = request.form.get('content')

    db.homework.update_one({'idx': int(idx)}, {'$set': {'title':title, 'content':content}})
    # todo
    return {"result": "success"}

# Delete
@app.route('/article', methods=['DELETE'])
def delete_article():
    idx = request.args.get('idx')
    db.article.delete_one({'idx':int(idx)})
    # todo
    return {"result": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)