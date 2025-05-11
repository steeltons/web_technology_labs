from config import ma, db
from marshmallow import fields, post_load
from building_views_models import Building, City, TypeBuilding

class CitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = City

    id = ma.auto_field()
    name = ma.auto_field()

class TypeBuilding(ma.SQLAlchemySchema):
    class Meta:
        model = TypeBuilding

    id = ma.auto_field()
    type = ma.auto_field()

class BuildingSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Building
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    title = ma.auto_field()
    year = ma.auto_field()
    height = ma.auto_field()
    city = ma.Nested(CitySchema())
    type_building = ma.Nested(TypeBuilding())

class BuildingDeserializer(ma.Schema):
    title = fields.Str(required=True, error_messages={"required": "title wasn't found"})
    year = fields.Integer(required=False, load_default=0)
    height = fields.Float(required=False, load_default=0.0)
    type_building_id = fields.Int(required=True, error_messages={"required": "type_building_id wasn't found"})
    city_id = fields.Int(required=True, error_messages={"required": "city_id wasn't found"})

    @post_load
    def make_building(self, data, **kwargs):
        return Building(**data)

class BuildingUpdateDeserializer(ma.Schema):
    title = fields.Str()
    year = fields.Integer()
    height = fields.Float()

    @post_load
    def make_building(self, data, **kwargs):
        return Building(**data)

building_schema = BuildingSchema()
building_schemas = BuildingSchema(many= True)
building_deserializer = BuildingDeserializer()
building_update_deserializer = BuildingUpdateDeserializer()
