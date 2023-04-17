import random
from pytest_voluptuous import S
from src.base_classes import BasicHttpMethods, APITestEndpoints
from src.payloads import JsonData


class TestApi:

    def test_ping_healthcheck(self):
        """A simple health check endpoint to confirm whether the API is up and running."""

        response = BasicHttpMethods.get(APITestEndpoints.url_ping)
        assert response.status_code == 201, f'Expected 200 status code, got {response.status_code} instead'

    def test_create_token(self):
        """Creates a new auth token to use for access to the PUT and DELETE /booking."""

        response = BasicHttpMethods.post(APITestEndpoints.url_auth, body=JsonData.json_auth)
        json_value_expected = "token"
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
        assert json_value_expected in response.json(), f"{response.json()} != {json_value_expected}"

    def test_get_all_booking_ids(self):
        """Returns the ids of all the bookings that exist within the API."""

        response = BasicHttpMethods.get(APITestEndpoints.url_get_booking)
        list_of_all_bookings = response.json()
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
        assert len(list_of_all_bookings) > 0, f'{list_of_all_bookings} is empty'

    def test_get_booking_by_name(self):
        """Returns a specific booking based upon the first name & last name provided."""

        response = BasicHttpMethods.get(
            APITestEndpoints.url_get_booking + f'?firstname={JsonData.json_get_booking_by_name["firstname"]}&lastname={JsonData.json_get_booking_by_name["lastname"]}')
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
        for booking_id in response.json():
            assert 'bookingid' in booking_id, 'No matching entries found'

    def test_get_booking_by_checkin_checkout(self):
        """Returns a specific booking based upon both checkin and checkout dates provided."""

        response = BasicHttpMethods.get(
            APITestEndpoints.url_get_booking + f'?checkin={JsonData.json_get_booking_by_dates["checkin"]}&checkout={JsonData.json_get_booking_by_dates["checkout"]}')
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'

    def test_get_booking_by_id(self):
        """Returns a specific booking based upon the booking id provided / Validates response's json schema."""

        response = BasicHttpMethods.get(APITestEndpoints.url_get_booking + f'/{random.randint(1, 100)}')
        data = response.json()
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
        assert S(
            JsonData.json_schema_get_specific_booking) == data, \
            f'Expected {S(JsonData.json_schema_get_specific_booking)}, got {data} instead '

    def test_create_booking(self):
        """Creates a new booking in the API / Verifies that new booking has been created."""

        response = BasicHttpMethods.post(APITestEndpoints.url_get_booking, body=JsonData.json_booking_form)
        json_value_expected = "bookingid"
        assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
        assert json_value_expected in response.json(), f"{response.json()} != {json_value_expected}"
        assert response.json()['bookingid'] != '', 'No new booking information'

    def test_update_booking(self):
        """Updates a current booking / Verifies the booking has been updated."""

        # 1) Creating new auth token for getting access to PUT method. Asserting that token has been created.

        auth_response = BasicHttpMethods.post(APITestEndpoints.url_auth, body=JsonData.json_auth)
        json_value_expected = auth_response.json()["token"]
        assert auth_response.status_code == 200, f'Expected 200 status code, got {auth_response.status_code} instead'
        assert 'token' in auth_response.json(), f'No token created in {auth_response.json()}'

        # 2) Get information about existing booking before further updating. Asserting response's status code.

        response_before_update = BasicHttpMethods.get(APITestEndpoints.url_get_booking + '/3')
        initial_data = response_before_update.json()
        assert response_before_update.status_code == 200, f'Expected 200 status code, got ' \
                                                          f'{response_before_update.status_code} instead '

        # 3) Updating booking's info by sending created token in cookies. Asserting response's status code.

        updated_response = BasicHttpMethods.put(APITestEndpoints.url_get_booking + '/3', body=JsonData.json_update_form,
                                                cookies={'token': json_value_expected})
        assert updated_response.status_code == 200, f'Expected 200 status code, got ' \
                                                    f'{updated_response.status_code} instead '

        # 4) Getting bookings info after updating. Comparing both info samples to verify the updates have taken place.

        updated_booking = BasicHttpMethods.get(APITestEndpoints.url_get_booking + '/3')
        updated_data = updated_booking.json()

        assert initial_data != updated_data, 'Data has not been updated'

    def test_booking_partial_update(self):
        """Updates a current booking with a partial payload / Verifies the booking has been partially updated."""

        # 1) Creating new auth token for getting access to PATCH method. Asserting that token has been created.

        auth_response = BasicHttpMethods.post(APITestEndpoints.url_auth, body=JsonData.json_auth)
        json_value_expected = auth_response.json()["token"]
        assert auth_response.status_code == 200, f'Expected 200 status code, got {auth_response.status_code} instead'
        assert 'token' in auth_response.json(), f'No token created in {auth_response.json()}'

        # 2) Get information about existing booking before further updating. Asserting response's status code.

        response_before_update = BasicHttpMethods.get(APITestEndpoints.url_get_booking + '/4')
        initial_data = response_before_update.json()
        assert response_before_update.status_code == 200, f'Expected 200 status code, got ' \
                                                          f'{response_before_update.status_code} instead '

        # 3) Partially updating booking's info by sending selected values and created token in cookies. Asserting
        # response's status code.

        partial_updated_response = BasicHttpMethods.patch(APITestEndpoints.url_get_booking + '/4',
                                                          body=JsonData.json_partial_update_form,
                                                          cookies={'token': json_value_expected})
        assert partial_updated_response.status_code == 200, f'Expected 200 status code, got ' \
                                                            f'{partial_updated_response.status_code} instead '

        # 4) Getting bookings info after updating. Comparing both info samples to verify the updates have taken place.

        updated_booking = BasicHttpMethods.get(APITestEndpoints.url_get_booking + '/3')
        updated_data = updated_booking.json()

        assert initial_data["firstname"] != updated_data, 'Selected value has not been updated'
        assert initial_data["lastname"] != updated_data, 'Selected value has not been updated'

    def test_delete_booking(self):
        """Deletes a specific booking based upon the booking id provided / Verifies booking has been deleted."""

        # 1) Creating new auth token for getting access to DELETE method. Asserting that token has been created.
        auth_response = BasicHttpMethods.post(APITestEndpoints.url_auth, body=JsonData.json_auth)
        json_value_expected = auth_response.json()["token"]
        assert auth_response.status_code == 200, f'Expected 200 status code, got {auth_response.status_code} instead'
        assert 'token' in auth_response.json(), f'No token created in {auth_response.json()}'

        # 2) Deleting booking by id. Asserting status code is 201

        response = BasicHttpMethods.delete(APITestEndpoints.url_get_booking + '/12',
                                           cookies={"token": json_value_expected})
        assert response.status_code == 201, f'Expected 201 status code, got {response.status_code} instead'

        # 3) Asserting that chosen booking was deleted

        response_after_deleting = BasicHttpMethods.get(APITestEndpoints.url_get_booking + '/12')
        assert response_after_deleting.status_code == 404, f'Expected 404 status code, ' \
                                                           f'got {response_after_deleting.status_code} instead'
