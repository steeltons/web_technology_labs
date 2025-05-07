from app import app
from flask import render_template
from structures.models import find_all_buildings, find_all_type_building_with_min_max_avh_height, find_all_country_buildings_order_by_county_name, find_all_building_stats_by_year_order_by_year, find_all_type_buildings_stats_type_similar, find_height_stats_for_countries_with_multiple_buildings


@app.route('/', methods=['GET'])
def index():
    [buildings_head, buildings_body] = find_all_buildings()
    [type_buildings_head, type_buildings_body] = find_all_type_building_with_min_max_avh_height()
    [country_stats_head, country_stats_body] = find_all_country_buildings_order_by_county_name()
    [building_year_stats_head, building_year_stats_body] = find_all_building_stats_by_year_order_by_year()
    [type_building_similar_head, type_building_similar_body] = find_all_type_buildings_stats_type_similar('мачта')
    [city_multiple_buildings_stats_head, city_multiple_buildings_stats_body] = find_height_stats_for_countries_with_multiple_buildings()

    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body,
        type_buildings_head=type_buildings_head,
        type_buildings_body=type_buildings_body,
        country_stats_head=country_stats_head,
        country_stats_body=country_stats_body,
        building_year_stats_head=building_year_stats_head,
        building_year_stats_body=building_year_stats_body,
        type_building_similar_head=type_building_similar_head,
        type_building_similar_body=type_building_similar_body,
        city_multiple_buildings_stats_head=city_multiple_buildings_stats_head,
        city_multiple_buildings_stats_body=city_multiple_buildings_stats_body
    )

    return html