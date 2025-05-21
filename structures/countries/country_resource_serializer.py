from models import Country
from app import ma

from marshmallow import fields, post_load


class CountryResourceSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    id = ma.auto_field()
    name = ma.auto_field()

    _links = ma.Hyperlinks({
        'self': ma.URLFor('countryresource', values= dict(id="<id>")),
        'collection' : ma.URLFor('countrylistresource'),
        'update' : ma.URLFor('countryresource', values= dict(id="<id>")),
        'delete' : ma.URLFor('countryresource', values= dict(id="<id>")),
    })

class CountryResourceDeserializer(ma.Schema):
    name = fields.Str(required=True, error_messages={"required": "Name is required"})

    @post_load
    def create_object(self, data, **kwargs):
        return Country(**data)

country_resource_serializer = CountryResourceSerializer()
countries_resource_serializer = CountryResourceSerializer(many=True)
country_resource_deserializer = CountryResourceDeserializer()