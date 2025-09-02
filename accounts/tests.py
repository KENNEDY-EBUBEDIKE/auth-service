from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'full_name': 'Kennedy Eziechina',
            'email': 'kennedyeziechina@gmail.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='kennedyeziechina@gmail.com').exists())

    def test_user_registration_password_mismatch(self):
        self.user_data['password_confirm'] = 'DifferentPassword'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        # Create first user
        self.client.post(self.register_url, self.user_data)
        # Try to create another user with same email
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            password='TestPassword123!'
        )

    def test_user_login_success(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetTestCase(APITestCase):
    def setUp(self):
        self.forgot_password_url = reverse('forgot_password')
        self.reset_password_url = reverse('reset_password')
        self.user = User.objects.create_user(
            email='reset@example.com',
            full_name='Reset User',
            password='OldPassword123!'
        )

    def test_forgot_password_success(self):
        data = {'email': 'reset@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_forgot_password_invalid_email(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reset_password_success(self):
        # First, get a reset token
        forgot_response = self.client.post(self.forgot_password_url, {'email': 'reset@example.com'})
        token = forgot_response.data['token']

        # Then, reset password
        reset_data = {
            'token': token,
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_invalid_token(self):
        reset_data = {
            'token': 'invalid_token',
            'new_password': 'NewPassword123!',
            'new_password_confirm': 'NewPassword123!'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)