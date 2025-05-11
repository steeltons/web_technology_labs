from config import ma
from marshmallow import fields, post_load
from models import City


class CitySerializer(ma.SQLAlchemySchema):
    class Meta:
        model = City

    id = ma.auto_field()
    name = ma.auto_field()
    country_id = ma.auto_field()

class CityDeserializer(ma.Schema):
    name = fields.Str(required=True, error_messages={"required": "Name wasn't provided"})
    country_id = fields.Integer(required=True, error_messages={"required": "Country id wasn't provided"})

    @post_load
    def make_obj(self, data, **kwargs):
        return City(**data)

class CityUpdateDeserializer(ma.Schema):
    name = fields.Str(required=True, error_messages={"required": "Name wasn't provided"})

    @post_load
    def make_obj(self, data, **kwargs):
        return City(**data)

city_serializer = CitySerializer()
cities_serializer = CitySerializer(many=True)
city_deserializer = CityDeserializer()
city_update_deserializer = CityUpdateDeserializer()