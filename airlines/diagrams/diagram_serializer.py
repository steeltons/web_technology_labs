from config import ma
from marshmallow import fields, post_load
from airlines.diagrams.diagram_dto import GetCountryStatsRqDto
from models import FlightStatus

class GetAllCountriesRqDtoDeserializer(ma.Schema):
    flight_status = fields.Enum(
        FlightStatus,
        data_key="flightStatus",
        attribute="flight_status"
    )

    @post_load
    def make_dto(self, data, **kwargs):
        print("Deserialized data:", data)  # 🔍 Печать словаря
        return GetCountryStatsRqDto(**data)

get_all_countries_stats_deserializer = GetAllCountriesRqDtoDeserializer()