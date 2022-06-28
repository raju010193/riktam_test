from rest_framework.test import APITestCase
from faker import Faker
from ..models import AppUser
from django.urls import reverse
from rest_framework import status
# fake = Faker()


class Base(APITestCase):
    fake = Faker()
    password = 'Test@123'
    token = ""
    username = ""

    def setUp(self) -> None:
        url = reverse('user_login')

        app_user = AppUser(username='admin', is_staff=True)
        app_user.set_password('12345')
        app_user.save()
        data = {'username': 'admin', "password": '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data.get('data').get('token').get('access_token')
        self.first_name = self.fake.name()
        self.last_name = self.fake.name()
        self.username = f"{self.first_name.replace(' ', '')}{self.last_name.replace(' ', '')}".lower()
