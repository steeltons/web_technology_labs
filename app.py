from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.json.ensure_ascii = False
auth = HTTPBasicAuth()

@app.route('/', methods= ['GET'])
def init_page():
  return jsonify({'app': 'Самые высокие здания и сооружения'})

if __name__ == 'main':
  app.run(debug=True)

from structures.buildings.views import *
from structures.error_handler.error_handler import *
from security.basic_auth_config import *