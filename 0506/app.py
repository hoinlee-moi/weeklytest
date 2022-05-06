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
    post = db.test.find_one({'idx': int(idx)}, {'_id': False})
    return render_template("detail.html", post=post)
    # todo

@app.route('/articleList', methods=['GET'])
def get_article_list():
    article_list = list(db.homework.find({}, {'_id': False}).sort('_id', -1))
    return jsonify({"article_list": article_list})

# Create
@app.route('/article', methods=['POST'])
def create_article():
    # todo
    if 0 >= db.homework.estimated_document_count():
        idx = 1
    else:
        idx = list(db.homework.find({}, sort=[('_id', -1)]).limit(1))[0]['idx'] + 1

    today = datetime.now()
    title_give = request.form['title']
    content_give = request.form['content']
    pw_give = request.form['pw']
    reg_date = today.strftime('%Y년%m월%d일 %H시%M분%S초')


    doc={
        'idx': idx,
        'title':title_give,
        'content':content_give,
        'pw': pw_give,
        'date':reg_date,
        'read_count': 0
    }

    db.homework.insert_one(doc)
    return {"result": "success"}

# Read
@app.route('/article', methods=['GET'])
def read_article():
    article = 0 #todo
    return jsonify({"article": article})

# Update
@app.route('/article', methods=['PUT'])
def update_article():
    # todo
    return {"result": "success"}

# Delete
@app.route('/article', methods=['DELETE'])
def delete_article():
    # todo
    return {"result": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)