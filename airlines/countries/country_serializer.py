from config import ma
from marshmallow import fields, post_load
from models import Country

class CountrySerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()
    continent_id = ma.auto_field()

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_country_by_id', values=dict(id="<id>")),
        'collection': ma.URLFor('get_all_countries'),
        'update': ma.URLFor('update_existing_country', values=dict(id='<id>')),
        'delete': ma.URLFor('delete_existing_country', values=dict(id='<id>')),
    })

class CountryUpdateDeserializer(ma.Schema):
    name = fields.String()
    code = fields.String()
    continent_id = fields.Integer()

    @post_load
    def make_country(self, data, **kwargs):
        return Country(**data)

class CountryCreateDeserializer(ma.Schema):
    name = fields.String(required=True)
    code = fields.String(required=True)
    continent_id = fields.Integer(required=True)

    @post_load
    def make_country(self, data, **kwargs):
        return Country(**data)

country_serializer = CountrySerializer()
country_update_deserializer = CountryUpdateDeserializer()
country_list_serializer = CountrySerializer(many=True)
country_create_deserializer = CountryCreateDeserializer()