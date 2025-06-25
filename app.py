from flask import Flask

app = Flask(__name__)

from airlines.error_handler.error_handler import *
from structures.views import *
from airlines.continents.continent_view import *
from airlines.countries.country_view import *
from airlines.pilots.pilot_view import *
from airlines.airports.airport_view import *
from airlines.flights.flight_view import *
from airlines.diagrams.diagram_view import *
from airlines.countryimages.country_image_view import *

if __name__ == 'main':
  app.run(debug=True)

