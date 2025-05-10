from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/', methods= ['GET'])
def init_page():
  return jsonify({'app': 'Самые высокие здания и сооружения'})

if __name__ == 'main':
  app.run(debug=True)

from structures.buildings.views import *
from structures.error_handler.error_handler import *