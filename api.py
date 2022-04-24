from flask import Flask, jsonify, escape, g, request
from flask_cors import CORS
import db_conn
from time import time
from twitter_api import get_tweets
import werkzeug
app = Flask(__name__)
# model 

CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADER"] = "Content-Type"

def page_not_found(e):
  return jsonify({
      "status": 0, 
      "message": "wrong path"}), 404

app.register_error_handler(404, page_not_found)

@app.before_request
def initialize_firebase():
    g.db = db_conn.initialize_db()


@app.route('/all_queries', methods=['GET', 'POST'])
def uui_request():
    body = request.get_json() if request.get_json() else request.args

    if 'uid' in body.keys():
        uid = body['uid']
        data = db_conn.get_all_searched_text(g.db, 'users', uid)
        return jsonify({
            "data": data,
            "status": 1
        })


# @app.route('/sentiment_data/<uid>', methods=['GET'])
# def get_sentiment_data(uid):
#     if hasattr(g, 'db'):

#         user_sentiment_data_list = db_conn.get_data_by_uid(
#             g.db, 'sentiment_data', uid)

#         if user_sentiment_data_list:
#             return jsonify({"data": user_sentiment_data_list})

#         return jsonify({"No Data": []})

#     return jsonify({"error": "No database connection"})


# @app.route('/sentiment_analysis', methods=['POST'])
# def analyze_data():
#     body = request.get_json()
#     text = body['text']
#     uid = body['uid']
#     start = time()
#     data = db_conn.analyze_text(g.db, u'users', uid, text)

#     return jsonify({
#         "data": data,
#         "execution_time": time() - start,
#         "status": 1})

@app.route('/topic/<topic>', methods=['GET', 'POST'])
def get_topic_data(topic):
    if hasattr(g, 'db'):
        data = db_conn.get_data_by_topic(g.db, 'twitter_topics', topic)
        
        if data:
            return jsonify({"data": data, "status": 1})
        else:
            return jsonify({"data": [], "status": 0, "error": "No data found"})

    return jsonify({"data": [], "status": 0, "error": "No database connection"})


@app.route('/all_topics', methods=['GET', 'POST'])
def all_topics():
    if hasattr(g, 'db'):
        data = db_conn.get_all_topics(g.db, 'twitter_topics')
        
        if data:
            return jsonify({"data": data, "status": 1})
        else:
            return jsonify({"data": [], "status": 0, "error": "No data found"})

    return jsonify({"data": [], "status": 0, "error": "No database connection"})

@app.route('/twitter_api', methods=['GET', 'POST'])
def analyze_tweet_topic():
    body = request.get_json() if request.get_json() else request.args
    

    if 'uid' in body.keys() and 'topic' in body.keys() and 'limit' in body.keys():
        uid = body['uid']
        topic = body['topic']
        limit = int(body['limit']) if str(body['limit']).isnumeric() else -100
        
        if 10 > limit or limit > 100:
            return jsonify({
                "data": [],
                "error": "Limit must be between 10 and 100 and a multiple of 10",
                "status": 0})
        start = time()
        try:
            text_array = get_tweets(topic, limit)
            algorithm = body['algorithm'] if 'algorithm' in body.keys() else 'vader'
            print(algorithm)
            data = db_conn.analyze_text_twitter(g.db, u'users', uid, text_array, topic,algorithm)
            return jsonify({
                "data": data,
                "execution_time": time() - start,
                "status": 1})
        except Exception as e:
            return jsonify({
                "data": [],
                "error": str(e),
                "status": 0})
    else:
        return jsonify({
            "data": [],
            "error": "Missing parameters",
            "status": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
