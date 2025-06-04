from app import app
from flask import render_template
from structures.models import *

@app.route('/', methods=['GET'])
def index():

    [flight_full_info_head, flight_full_info_body] = find_all_flights_with_airports_and_countries()
    [pilot_info_header, pilot_info_body] = find_all_pilots_departure_arrive_continent_same()
    [countries_arrival_avg_head, countries_arrival_avg_body] = find_all_countries_arrival_greater_than_avg()
    [countries_min_max_avg_header, countries_min_max_avg_body] = find_all_countries_with_min_max_avg()
    [flight_min_max_head, flight_min_max_body] = find_all_min_max_avg_flight_airports()

    return render_template('index.html',
                           flight_full_info_head= flight_full_info_head,
                           flight_full_info_body= flight_full_info_body,
                           pilot_info_header= pilot_info_header,
                           pilot_info_body= pilot_info_body,
                           countries_arrival_avg_head= countries_arrival_avg_head,
                           countries_arrival_avg_body= countries_arrival_avg_body,
                           countries_min_max_avg_header= countries_min_max_avg_header,
                           countries_min_max_avg_body= countries_min_max_avg_body,
                           flight_min_max_head= flight_min_max_head,
                           flight_min_max_body= flight_min_max_body,
                           )