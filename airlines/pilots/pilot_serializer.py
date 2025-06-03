from config import ma
from marshmallow import fields, post_load
from models import Pilot

class PilotSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Pilot

    id = ma.auto_field()
    name = ma.auto_field()

    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_pilot_by_id', values=dict(id="<id>")),
        'collection': ma.URLFor('get_all_pilots'),
        'update': ma.URLFor('update_existing_pilot', values=dict(id='<id>')),
        'delete': ma.URLFor('delete_existing_pilot', values=dict(id='<id>')),
    })

class PilotUpdateDeserializer(ma.Schema):
    name = fields.String()

    @post_load
    def make_pilot(self, data, **kwargs):
        return Pilot(**data)

class PilotCreateDeserializer(ma.Schema):
    name = fields.String(required=True)

    @post_load
    def make_pilot(self, data, **kwargs):
        return Pilot(**data)

pilot_serializer = PilotSerializer()
pilot_update_deserializer = PilotUpdateDeserializer()
pilot_list_serializer = PilotSerializer(many=True)
pilot_create_deserializer = PilotCreateDeserializer()
