from django.urls import reverse
from rest_framework import status
from ..tests.base import Base
from ..models import AppUser
from django.utils.http import urlencode


# Create your tests here.
# class Base(object):

class ChatTests(Base):
    """
    Chat Test cases
    """
    login_user_token = ""

    def setUp(self) -> None:
        super().setUp()
        # url = reverse('register')
        # self.token = response.data.get('data').get('token').get('access_token')
        self.second_user_first_name = self.fake.name()
        self.second_user_last_name = self.fake.name()
        self.second_user_username = f"{self.second_user_first_name.replace(' ', '')}{self.second_user_last_name.replace(' ', '')}".lower()

    def create_account(self, data):
        """
        Create account
        @param data
        """
        url = reverse('register')

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        return response

    def test_send_message(self):
        """
        send message test case
        one to one message
        """
        first_user_data = {'first_name': self.first_name,
                           'last_name': self.last_name, 'username': self.username,
                           'email': f"{self.username}@gmail.com",
                           "password": self.password}
        second_user_data = {'first_name': self.second_user_first_name,
                            'last_name': self.second_user_last_name, 'username': self.second_user_username,
                            'email': f"{self.second_user_username}@gmail.com",
                            "password": self.password}
        self.create_account(first_user_data)
        self.create_account(second_user_data)
        url = reverse('user_login')
        self.client.credentials(
            HTTP_AUTHORIZATION='')
        data = {'username': self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        self.login_user_token = token
        user_url = reverse('users')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(user_url, format='json')
        data = response.data.get('data')
        status_code = 404
        if data:
            second_user_uuid = data[0].get('uuid')
            status_code = 200
        self.assertEqual(status_code, status.HTTP_200_OK)
        send_message_url = reverse('send_messages')
        data = {
            'receiver_id': second_user_uuid,
            "message": self.fake.text()
        }
        response = self.client.post(send_message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_send_message(self):
        """
        Get sent messages
        """
        first_user_data = {'first_name': self.first_name,
                           'last_name': self.last_name, 'username': self.username,
                           'email': f"{self.username}@gmail.com",
                           "password": self.password}
        second_user_data = {'first_name': self.second_user_first_name,
                            'last_name': self.second_user_last_name, 'username': self.second_user_username,
                            'email': f"{self.second_user_username}@gmail.com",
                            "password": self.password}
        self.create_account(first_user_data)
        self.create_account(second_user_data)
        url = reverse('user_login')
        self.client.credentials(
            HTTP_AUTHORIZATION='')
        data = {'username': self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        self.login_user_token = token
        user_url = reverse('users')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(user_url, format='json')
        data = response.data.get('data')
        status_code = 404
        if data:
            second_user_uuid = data[0].get('uuid')
            status_code = 200
        self.assertEqual(status_code, status.HTTP_200_OK)
        send_message_url = reverse('send_messages')
        data = {
            'receiver_id': second_user_uuid,
            "message": self.fake.text()
        }
        response = self.client.post(send_message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        send_message_url = reverse('send_messages')
        send_message_url = f"{send_message_url}?receiver_id={second_user_uuid}"
        # receiver_id = second_user_uuid
        response = self.client.get(send_message_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
