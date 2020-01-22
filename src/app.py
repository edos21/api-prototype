from flask import Flask, request, jsonify
from datetime import date
import uuid 

app = Flask(__name__)

reviews = []

@app.route('/v1/review/', methods=['POST'])
def create_review():
  body = request.get_json()
  if next(filter(lambda x: x['sale_id'] == body['sale_id'], reviews), None):
    return {'message': "A review for the sale '{}' already exists.".format(body['sale_id'])}, 400
  
  review = {
      "id": uuid.uuid1().int,
      "sale_id": body['sale_id'],
      "store_id": body['store_id'],
      "user_id": body['user_id'],
      "review": body['review'],
      "score": body['score'],
      "date": date.today(),
      "is_deleted": False,
  }
  reviews.append(review)
  return jsonify(review)

app.run(port=5000)