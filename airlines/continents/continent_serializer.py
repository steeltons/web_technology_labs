from sqlalchemy import values

from config import ma
from marshmallow import fields, post_load
from models import Continent

class ContinentSerializer(ma.SQLAlchemySchema):

    class Meta:
        model = Continent

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_continent_by_id', values=dict(id= "<id>")),
        'collection': ma.URLFor('get_all_continents'),
        'update': ma.URLFor('update_existing_continent', values=dict(id= '<id>')),
        'delete': ma.URLFor('delete_existing_continent', values=dict(id= '<id>')),
    })

class ContinentUpdateDeserializer(ma.SQLAlchemySchema):

    id = fields.Integer(required=True, error_messages={'required': 'ID is required'})
    name = fields.String()
    code = fields.String()

    @post_load
    def make_continent(self, data, **kwargs):
        return Continent(**data)

class ContinentCreateDeserializer(ma.Schema):

    name = fields.String(required=True, error_messages={'required': 'Name is required'})
    code = fields.String(required=True, error_messages={'required': 'Code is required'})

    @post_load
    def make_object(self, data, **kwargs):
        return Continent(**data)

continent_serializer = ContinentSerializer()
continent_update_deserializer = ContinentUpdateDeserializer()
continent_list_serializer = ContinentSerializer(many=True)
continent_create_deserializer = ContinentCreateDeserializer()