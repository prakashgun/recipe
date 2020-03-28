from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserPublicApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user eih payload"""
        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'some name'
        }
        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating already exist user fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'some name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Validate password before creating the user"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'some name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Check user not created
        user_exists = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user_exists)

    def create_token_for_user(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pass',
            'name': 'some name'
        }

        create_user(**payload)

        del payload['name']

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test toke is not created when invaid credentials are given"""

        payload = {
            'email': 'test@example.com',
            'password': 'pass',
            'name': 'some name'
        }

        create_user(**payload)
        del payload['name']
        payload['password'] = 'wrong'
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        res = self.client.post(TOKEN_URL,
                               {'email': 'test@example.com', 'password': ''}
                               )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
