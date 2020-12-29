from django.test import TestCase

# Create your tests here.
from notifications.models import Notification
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def testAdmin(self):
        client = APIClient()
        response = client.get('admin/')
        print(response)