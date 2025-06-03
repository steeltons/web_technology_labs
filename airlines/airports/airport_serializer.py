from config import ma
from marshmallow import fields, post_load
from models import Airport

class AirportSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Airport

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()
    country_id = ma.auto_field()

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_airport_by_id', values=dict(id="<id>")),
        'collection': ma.URLFor('get_all_airports'),
        'update': ma.URLFor('update_existing_airport', values=dict(id='<id>')),
        'delete': ma.URLFor('delete_existing_airport', values=dict(id='<id>')),
    })

class AirportUpdateDeserializer(ma.Schema):
    name = fields.String()
    code = fields.String()
    country_id = fields.Integer()

    @post_load
    def make_airport(self, data, **kwargs):
        return Airport(**data)

class AirportCreateDeserializer(ma.Schema):
    name = fields.String(required=True)
    code = fields.String(required=True)
    country_id = fields.Integer(required=True)

    @post_load
    def make_airport(self, data, **kwargs):
        return Airport(**data)

airport_serializer = AirportSerializer()
airport_update_deserializer = AirportUpdateDeserializer()
airport_list_serializer = AirportSerializer(many=True)
airport_create_deserializer = AirportCreateDeserializer()