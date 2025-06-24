from config import ma
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from models import Flight, FlightStatus, Airport


class DepartureAirportUi(ma.SQLAlchemySchema):
    class Meta:
        model = Airport

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()
    country_id = ma.auto_field()

class FlightSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Flight

    id = ma.auto_field()
    departure_date = ma.auto_field()
    flight_status = EnumField(FlightStatus)
    departure_airport_id = ma.auto_field()
    arrival_airport_id = ma.auto_field()
    pilot_id = ma.auto_field()

    def get_status(self, obj):
        return obj.flight_status.name

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_flight_by_id', values=dict(id="<id>")),
        'collection': ma.URLFor('get_all_flights'),
        'update': ma.URLFor('update_existing_flight', values=dict(id='<id>')),
        'delete': ma.URLFor('delete_existing_flight', values=dict(id='<id>')),
    })

class FlightUiSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Flight
        load_instance = True

    id = ma.auto_field()
    departure_date = ma.auto_field()
    flight_status = EnumField(FlightStatus).display_name
    departure_airport = ma.auto_field()

class FlightUpdateDeserializer(ma.Schema):
    departure_date = fields.Date()
    flight_status = fields.String()
    departure_airport_id = fields.Integer()
    arrival_airport_id = fields.Integer()
    pilot_id = fields.Integer()

    @post_load
    def make_flight(self, data, **kwargs):
        if 'flight_status' in data:
            data['flight_status'] = FlightStatus[data['flight_status']]
        return Flight(**data)

class FlightCreateDeserializer(ma.Schema):
    departure_date = fields.Date(required=True)
    flight_status = EnumField(FlightStatus, load_default=FlightStatus.UNKNOWN)
    departure_airport_id = fields.Integer(required=True)
    arrival_airport_id = fields.Integer(required=True)
    pilot_id = fields.Integer(required=True)

    @post_load
    def make_flight(self, data, **kwargs):
        return Flight(**data)

flight_serializer = FlightSerializer()
flight_update_deserializer = FlightUpdateDeserializer()
flight_list_serializer = FlightSerializer(many=True)
flight_create_deserializer = FlightCreateDeserializer()
