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

    return {"result": "success"}

@app.route('/post', methods=['POST'])
def save_post():
    if 0 >= db.homework.estimated_document_count():
        idx = 1
    else:
        idx = list(db.homework.find({}, sort=[('_id', -1)]).limit(1))[0]['idx'] + 1

    title = request.form['title_give']
    pw = request.form['pw_give']
    comment = request.form['comment_give']
    today = datetime.now()
    reg_date = today.strftime('%Y년%m월%d일 %H시%M분%S초')

    doc = {
        'idx':idx,
        'title':title,
        'pw':pw,
        'content':comment,
        'reg_date':reg_date
    }
    db.homework.insert_one(doc)


    return jsonify({'result': 'success', 'msg': '포스팅 완료!'})


@app.route('/post', methods=['GET'])
def get_post():
    posts = list(db.homework.find({}, {'_id': False}).sort('_id', -1))

    return jsonify({"posts": posts})


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx = request.args.get('idx')
    db.test.delete_one({'idx': int(idx)})
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)