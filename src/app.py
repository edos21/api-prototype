'''
  App file for 'Pedidos Ya' Backend technical test.
  This is the prototype implementation for the proposed scenario.
  It was made with Python using Flask as framework, runing on http://127.0.0.1:5000/
  it has no Database so all Reviews will be saved locally and will be lost when the
  local server quits.

  The variables and methods name used are self explanatory
  for any doubt, don't hessitate on contacting me
  Author: Eduardo Sanchez (edos21@gmail.com)

  The API Documentation can be found at https://documenter.getpostman.com/view/257959/SWT8fe3i?version=latest
'''
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid 

app = Flask(__name__)

reviews = [] #local storage for the created Reviews


@app.route('/v1/review/', methods=['POST'])
def create_review():
  body = request.get_json()
  if next(filter(lambda x: x['sale_id'] == body['sale_id'], reviews), None):
    return {'message': f"Sale '{body['sale_id']}' has already been reviewed."}, 400
  
  review = {
      "id": uuid.uuid1().int,
      "sale_id": body['sale_id'],
      "store_id": body['store_id'],
      "user_id": body['user_id'],
      "review": body['review'],
      "score": body['score'],
      "date": datetime.today(),
      "is_deleted": False,
  }

  reviews.append(review)
  return jsonify(review)

@app.route('/v1/review/<int:id>', methods=['DELETE'])
def delete_review(id):
  review = next(filter(lambda x: x['id'] == id and not x['is_deleted'], reviews), None)
  if review:
    review["is_deleted"] = True
    return {'message': "The review was deleted!"}

  return {'message': f"Review ID '{id}' does not exist."}, 404


@app.route('/v1/sale/<int:sale_id>/review', methods=['GET'])
def get_sale_review(sale_id):
    review = next(filter(lambda x: x['sale_id'] == sale_id and not x['is_deleted'], reviews), None)
    if not review:
      return {'message': f"Review for sale '{sale_id}' does not exist"}, 404

    return jsonify(review)


@app.route('/v1/store/<int:store_id>/reviews', methods=['GET'])
def get_store_reviews(store_id):
    date_format = '%Y%m%d'
    
    if request.args.get('from'):
      start_date = datetime.strptime(request.args.get('from'), date_format)
    else:
      start_date = datetime.today() - timedelta(days=30)

    if request.args.get('to'):
      end_date = datetime.strptime(request.args.get('to'), date_format)
    else:
      end_date = datetime.today()

    reviews_list = list(filter(lambda x: x['store_id'] == store_id and start_date <= x['date'] <= end_date
    and not x['is_deleted'], reviews))

    if not reviews_list:
      return {'message': f"There are no reviews for store '{store_id}' from date {start_date: %d/%m/%Y} to date {end_date: %d/%m/%Y}"}, 404
    return jsonify(reviews_list)

app.run(port=5000)