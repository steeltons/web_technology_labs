from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

app = Flask(__name__)
app.json.ensure_ascii = False
auth = HTTPBasicAuth()

api = Api(app)

@app.route('/', methods= ['GET'])
def init_page():
  return jsonify({'app': 'Самые высокие здания и сооружения'})

if __name__ == 'main':
  app.run(debug=True)

from structures.buildings.building_views import *
from structures.error_handler.error_handler import *
from security.basic_auth_config import *
from structures.cities.city_resource import *
from structures.type_buildings.type_building_resource import *
from structures.countries.country_resource import *