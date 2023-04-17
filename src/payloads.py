import random
from pytest_voluptuous import S
from voluptuous import Optional

from src.generator import DataGenerator, DateGenerator


class JsonData:
    """Contains payloads for https methods and json schema validation tests."""

    json_auth = {
        "username": "admin",
        "password": "password123"
    }

    json_get_booking_by_name = {
        'firstname': 'Sally',
        'lastname': 'Brown'
    }

    json_get_booking_by_dates = {
        'checkin': DateGenerator.checkin,
        'checkout': DateGenerator.checkout
    }

    json_schema_get_specific_booking = S({

        "firstname": str,
        "lastname": str,
        "totalprice": int,
        "depositpaid": bool,
        "bookingdates": {
            "checkin": str,
            "checkout": str
        },
        Optional("additionalneeds"): str,

    })

    json_booking_form = {
        "firstname": DataGenerator.first_name(),
        "lastname": DataGenerator.last_name(),
        "totalprice": random.randint(100, 5000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": DateGenerator.checkin,
            "checkout": DateGenerator.checkout
        },
        "additionalneeds": 'Ultra All Inclusive'
    }

    json_update_form = {

        "firstname": DataGenerator.first_name(),
        "lastname": DataGenerator.last_name(),
        "totalprice": random.randint(10, 20),
        "depositpaid": False,
        "bookingdates": {
            "checkin": DateGenerator.checkin,
            "checkout": DateGenerator.checkout
        },
        "additionalneeds": 'No bed, no breakfast'

    }
    json_partial_update_form = {
        "firstname": DataGenerator.first_name(),
        "lastname": DataGenerator.last_name()
    }
