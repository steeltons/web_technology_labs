from marshmallow import post_dump, fields
import base64
from config import ma
from models import CountryImage, Country, Continent


class ContinentSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Continent
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()


class CountrySerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Country
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    code = ma.auto_field()
    description = ma.auto_field()
    continentId = ma.auto_field("continent_id", data_key="continentId")
    continent = ma.Nested(ContinentSerializer)
    airportsCount = fields.Integer()
    flightsCount = fields.Integer()


class CountryImageSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = CountryImage
        load_instance = True

    id = ma.auto_field()
    imageData = fields.Method("get_image_base64")
    imageName = ma.auto_field("image_name", data_key="imageName")
    countryId = ma.auto_field("country_id", data_key="countryId")
    country = fields.Nested(CountrySerializer)

    def get_image_base64(self, obj):
        if obj.image_data:
            return base64.b64encode(obj.image_data).decode('utf-8')
        return None


serializer = CountryImageSerializer()
serializer_list = CountryImageSerializer(many=True)
