from exceptions import NotFoundException
from models import CountryImage, Country, Airport, Flight
from airlines.countryimages.country_image_deserializer import serializer, serializer_list
from sqlalchemy.orm import joinedload


def get_pageable_country_images(page: int | None, limit: int | None):
    query = CountryImage.query.options(
        joinedload(CountryImage.country).joinedload(Country.continent)
    )

    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    for image in paginated.items:
        country = image.country
        if country:
            country.airportsCount = Airport.query.filter_by(country_id=country.id).count()
            country.flightsCount = (
                Flight.query
                      .filter((Flight.departure_airport.has(country_id=country.id)) |
                        (Flight.arrival_airport.has(country_id=country.id))).count()
            )

    return {
        'data': serializer_list.dump(paginated.items),
        'totalElements': paginated.total,
        'currentPage': paginated.page,
        'totalPages': paginated.pages,
        'perPage': paginated.per_page,
    }


def get_country_image_by_id(image_id: int):
    country_image = CountryImage.query.options(
        joinedload(CountryImage.country).joinedload(Country.continent)
    ).get(image_id)

    if not country_image:
        raise NotFoundException(f"CountryImage was not found: id={image_id}")

    country = country_image.country
    if country:
        country.airportsCount = Airport.query.filter_by(country_id=country.id).count()
        country.flightsCount = Flight.query \
            .filter((Flight.departure_airport.has(country_id=country.id)) |
                    (Flight.arrival_airport.has(country_id=country.id))).count()

    return serializer.dump(country_image)
