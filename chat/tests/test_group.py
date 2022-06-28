from django.urls import reverse
from rest_framework import status
from ..tests.base import Base
from ..models import AppUser
from django.utils.http import urlencode


# Create your tests here.
# class Base(object):

class GroupChatTests(Base):
    """
    group and group Chat Test cases
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
        url = reverse('register')

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        return response

    def get_login(self, data):
        url = reverse('user_login')
        self.client.credentials(
            HTTP_AUTHORIZATION='')
        response = self.client.post(url, data, format='json')
        return response

    def create_group(self, token):
        url = reverse('group')

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'name': self.fake.name(),
            'group_info': self.fake.text()
        }
        response = self.client.post(url, data, format='json')
        return response

    def get_groups(self, token):
        url = reverse('group')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url, format='json')
        return response

    def get_users(self, token):
        user_url = reverse('users')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(user_url, format='json')
        return response

    def test_create_group(self):
        response = self.create_group(self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_group(self):
        first_user_data = {'first_name': self.first_name,
                           'last_name': self.last_name, 'username': self.username,
                           'email': f"{self.username}@gmail.com",
                           "password": self.password}
        self.create_account(first_user_data)
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.create_group(token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.get_groups(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('data')
        group_id = data[0].get('uuid')
        delete_url = f"{reverse('group')}?group_id={group_id}"
        response = self.client.delete(delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_group(self):
        first_user_data = {'first_name': self.first_name,
                           'last_name': self.last_name, 'username': self.username,
                           'email': f"{self.username}@gmail.com",
                           "password": self.password}
        self.create_account(first_user_data)
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        search = ""
        for _ in range(10):
            response = self.create_group(token)
            search = response.data.get('data').get('name')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        search_url = f"{reverse('group')}?search={search}"
        response = self.client.get(search_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_members_group(self):
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
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        response = self.create_group(token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.get_groups(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('data')
        group_id = data[0].get('uuid')
        response = self.get_users(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data.get('data')
        users_list = []
        for user in user_data:
            users_list.append(
                {
                    'member': user.get('uuid'),
                    'is_group_admin': False
                }
            )
        # group_id = data[0].get('uuid')
        data = {
            'group_id': group_id,
            'users_list': users_list
        }
        add_member_url = reverse('group_member')
        response = self.client.post(add_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_group_message(self):
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
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        response = self.create_group(token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.get_groups(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('data')
        group_id = data[0].get('uuid')
        response = self.get_users(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data.get('data')
        users_list = []
        for user in user_data:
            users_list.append(
                {
                    'member': user.get('uuid'),
                    'is_group_admin': False
                }
            )
        # group_id = data[0].get('uuid')
        data = {
            'group_id': group_id,
            'users_list': users_list
        }
        add_member_url = reverse('group_member')
        response = self.client.post(add_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        group_message_url = reverse('group_chat')
        data = {
            'group_id': group_id,
            'message': self.fake.text()
        }
        response = self.client.post(group_message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_group_message(self):
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
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')

        response = self.create_group(token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.get_groups(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('data')
        group_id = data[0].get('uuid')
        response = self.get_users(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data.get('data')
        users_list = []
        for user in user_data:
            users_list.append(
                {
                    'member': user.get('uuid'),
                    'is_group_admin': False
                }
            )
        # group_id = data[0].get('uuid')
        data = {
            'group_id': group_id,
            'users_list': users_list
        }
        add_member_url = reverse('group_member')
        response = self.client.post(add_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        group_message_url = reverse('group_chat')
        data = {
            'group_id': group_id,
            'message': self.fake.text()
        }
        response = self.client.post(group_message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(group_message_url + f"?group_id={group_id}", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_user(self):
        first_user_data = {'first_name': self.first_name,
                           'last_name': self.last_name, 'username': self.username,
                           'email': f"{self.username}@gmail.com",
                           "password": self.password}
        second_user_data = {'first_name': self.second_user_first_name,
                            'last_name': self.second_user_last_name, 'username': self.second_user_username,
                            'email': f"{self.second_user_username}@gmail.com",
                            "password": self.password}
        third_user_data = {'first_name': self.second_user_first_name,
                           'last_name': self.second_user_last_name, 'username': self.second_user_username + '1',
                           'email': f"{self.second_user_username}1@gmail.com",
                           "password": self.password}
        self.create_account(first_user_data)
        self.create_account(second_user_data)
        self.create_account(third_user_data)
        response = self.get_login({'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('data').get('token').get('access_token')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token)
        search_url = f"{reverse('users')}?search={self.username}"
        response = self.client.get(search_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
