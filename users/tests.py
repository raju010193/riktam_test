from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AppUser
from faker import Faker


# Create your tests here.
# class Base(object):

class AccountTests(APITestCase):
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

    def create_account(self):
        """
        Create account
        """
        url = reverse('register')
        data = {'first_name': self.first_name,
                'last_name': self.last_name, 'username': self.username, 'email': f"{self.username}@gmail.com",
                "password": self.password}
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_account(self):
        """
        create account test case
        """
        # url = reverse('register')
        response = self.create_account()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_accounts(self):
        url = reverse('register')
        self.create_account()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account(self):
        """
        Update account test case
        """
        url = reverse('register')
        self.create_account()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')
        data = response.data.get('data')
        status_code = 404
        if data:
            update_uuid = data[0].get('uuid')
            status_code = 200
        self.assertEqual(status_code, status.HTTP_200_OK)
        data = {'first_name': self.fake.name(),
                'uuid': update_uuid,
                'last_name': self.fake.name(), 'username': self.username, 'email': f"{self.username}@gmail.com",
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_account(self):
        """
        Delete account test case
        """
        url = reverse('register')
        self.create_account()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')
        data = response.data.get('data')
        status_code = 404
        if data:
            update_uuid = data[0].get('uuid')
            status_code = 200
        self.assertEqual(status_code, status.HTTP_200_OK)
        response = self.client.delete(f"{url}?uuid={update_uuid}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        """
        test Login test case
        """
        url = reverse('user_login')
        self.create_account()
        username = self.username
        self.client.credentials(
            HTTP_AUTHORIZATION='')
        data = {'username': username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """
        test logout test case
        """
        url = reverse('user_login')
        self.create_account()
        username = self.username
        self.client.credentials(
            HTTP_AUTHORIZATION='')
        data = {'username': username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data.get('data').get('token').get('refresh_token')
        access_token = response.data.get('data').get('token').get('access_token')
        logout_url = reverse('user_logout')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '+access_token)
        data = {
            'refresh':refresh_token
        }
        response = self.client.post(logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

