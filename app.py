from nlpUtils import TextSimilarity
import os
import pymongo
import urllib.parse
from flask import jsonify
from flask import request
from flask import Flask
import uuid
from bson import json_util
import operator
import json

app = Flask(__name__)

quote_simalarity_service = TextSimilarity()

# client = pymongo.MongoClient("mongodb+srv://devUser:MlIG8QwJSZJpusMq@cluster0.017ba.mongodb.net/quote?retryWrites=true&w=majority")
username = urllib.parse.quote_plus(os.environ.get('MONGO_DB_USERNAME'))
password = urllib.parse.quote_plus(os.environ.get('MONGO_DB_PASSWORD'))

client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.017ba.mongodb.net/quote?retryWrites=true&w=majority")
db = client.quotes
quote_collection = db.quotes

@app.route('/quote', methods=['GET'])
def get_all_quotes():
    return json_util.dumps(list(quote_collection.find({})))

@app.route('/quote', methods=['POST'] )
def add_quote():
    post_data = request.json
    if "quotes" in post_data and "author" in post_data:
        post_data["id"] = uuid.uuid1().__str__()
        if "rating" not in post_data:
            post_data["rating"] = ""
        
        inserted_id = quote_collection.insert_one(post_data).inserted_id
    else:
        return jsonify({"error_message" : "quotes and author is mandatory"})

    return jsonify({"id": post_data["id"]})


@app.route('/quote/<quote_id>', methods=['PUT'] )
def rate_quote(quote_id):
    post_data = request.json
    if 'rating' not in post_data:
        return jsonify({"error_message" : "rating is mandatory"})

    if  post_data['rating'] > 5 or post_data['rating'] < 0:
        return jsonify({"error_message" : "rating should be between 0 and 5"})

    try:
        filter = { 'id': quote_id }
        newvalues = { "$set": { 'rating': post_data['rating']} }
        quote_collection.update_one(filter, newvalues)
        cursor = quote_collection.find(filter) 
    except:
        return jsonify({"error_message" : "Error while saving ratings"})
    return json_util.dumps(list(cursor))


@app.route('/quote/<quote_id>', methods=['DELETE'] )
def delete_quote(quote_id):
    post_data = request.json
    if quote_id is None :
        return jsonify({"error_message" : "quote_id is mandatory"})

    try:
        myquery = { "id": quote_id }
        quote_collection.delete_one(myquery)

    except:
        return jsonify({"error_message" : "Error while deleting quote"})
    return jsonify({"status":"success"})


@app.route('/getRatedQuote', methods=['GET'])
def get_rated_quotes():
    return json_util.dumps(list(quote_collection.find({"rating": { "$gt": 3 } })))


@app.route('/getRelatedQuote', methods=['POST'])
def get_related_quotes():
    post_data = request.json
    
    if "quote" in post_data:
        unrelatedQuote = post_data['quote']
    else:
        acursor = quote_collection.find_one({"$or": [{"rating": {"$eq" : ""}}] })
        unrelatedQuote = acursor["quotes"]
    matchingScore = {}
    
    for acursor in  list(quote_collection.find({"rating": { "$gt": 3 } })):
        matchingScore[acursor["id"]] =  quote_simalarity_service.get_similarity_score(unrelatedQuote, acursor["quotes"] )

    id,score = max(matchingScore.items(), key=operator.itemgetter(1))
    ret = {}
    ret["quote"] = json.loads(json_util.dumps(list(quote_collection.find({"id": { "$eq":  id} }))))
    ret["matchingScore"] = score * 100
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)
