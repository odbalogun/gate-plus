from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from estates.models import Estate
import os

User = get_user_model()


class TestUser(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.uri = '/users/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        # save estate
        e = Estate.tenancy.create_estate(name="Test Estate", slug='test_estate')
        e.save()

        user = User.objects.create_user(email='testuser@test.com', first_name="Test First", last_name="Test Last",
                                        password='test')
        user.estate = e
        user.save()

        return user

    def test_signup(self):
        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'gateplus.dev:8000'
        self.uri = '/users/signup/'
        params = {
            "first_name": "Test First",
            "last_name": "Last Name",
            "email": "testuser@test.com",
            "password": "test",
            "estate": {
                "name": "Test Estate 2",
                "slug": "test_estate2"
            }
        }

        response = self.client.post(self.uri, params, format='json', SERVER_NAME='gateplus.dev:8000')
        # self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0}: {1} instead.'
        #                 .format(response.status_code, response.data))
        self.assertEqual(response.status_code, 201, "Expected Response Code 201, received {0}".format(response.status_code))

    def get_url(self):
        # print(self.client.get(self.uri))
        return self.client.get(self.uri)


