from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Reviews(Resource):
  def get(self, id):
    return {'id': id}

api.add_resource(Reviews, '/v1/review/<string:id>')

app.run(port=5000)