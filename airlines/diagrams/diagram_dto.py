from models import FlightStatus

class GetCountryStatsRqDto:

    def __init__(self, flight_status: FlightStatus = FlightStatus.UNKNOWN):
        self.flight_status = flight_status