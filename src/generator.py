from faker import Faker
from datetime import datetime, timedelta


class DataGenerator:
    """Generator of first and last name for booking form."""

    @staticmethod
    def first_name():
        fake = Faker()
        return fake.first_name()

    @staticmethod
    def last_name():
        fake = Faker()
        return fake.last_name()


class DateGenerator:
    """Generator of checkin and checkout dates."""
    @staticmethod
    def get_date():
        checkin = str(datetime.now().date())
        parse = datetime.strptime(checkin, '%Y-%m-%d')
        checkout = parse + timedelta(days=7)
        date = [checkin, checkout.strftime('%Y-%m-%d')]
        return date

    get_date = get_date()
    checkin = get_date[0]
    checkout = get_date[1]

