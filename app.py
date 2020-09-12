import json

from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'marketdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/marketdb'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/companies', methods=['GET'])
def get_all_companies():
  comp = mongo.db.companies
  output = []
  for c in comp.find():
    output.append({'name' : c['name']})
  return jsonify({'result' : output})


@app.route('/company', methods=['POST'])
def add_company():
  companies = mongo.db.company
  app.logger.info('request: ', request.data )
  data = json.loads(request.data)
  name = data.get('name')
  size = data.get('size')
  comp_id = companies.insert_many({'name': name, 'size': size})
  new_comp = companies.find_one({'_id': comp_id })
  output = {'name' : new_comp['name'], 'size' : new_comp['size']}
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
