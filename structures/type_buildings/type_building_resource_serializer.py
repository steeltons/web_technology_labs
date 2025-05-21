from sqlalchemy import values

from app import ma
from models import TypeBuilding

from marshmallow import fields, post_load

class TypeBuildingResourceSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = TypeBuilding

    id = ma.auto_field()
    type = ma.auto_field()

    _links = ma.Hyperlinks({
        'self' : ma.URLFor('typebuildingresource', values=dict(id="<id>")),
    })

class TypeBuildingResourceDeserializer(ma.Schema):
    type = fields.Str(required=True, error_messages={"required": "Type is required"})

    @post_load
    def create_objects(self, data, **kwargs):
        return TypeBuilding(**data)

type_building_serializer = TypeBuildingResourceSerializer()
type_buildings_serializer = TypeBuildingResourceDeserializer(many=True)
type_building_deserializer = TypeBuildingResourceDeserializer()