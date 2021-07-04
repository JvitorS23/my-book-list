from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:user-register')
LOGIN_URL = reverse('user:user-login')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@jvss.com',
            'name': 'jose',
            'password': 'test123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_invalid_user_fails(self):
        """Test creating user with invalid payload fails"""
        # Wrong email
        payload = {
            'email': 'test',
            'name': 'jose',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # No name provided
        payload = {
            'email': 'test@email.com',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # No email provided
        payload = {
            'name': 'jose',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """Test creating an user that already exists fails"""
        payload = {'email': 'test@jvss.com',
                   'password': 'test123',
                   'name': 'jose'
                   }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'jvss@email.com',
                   'name': 'jose',
                   'password': 'pw'
                   }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_user_login(self):
        """Test that user login success with valid credentials"""
        payload = {
            'email': 'jvss@email.com',
            'password': 'test123',
            'name': 'jose'
        }
        create_user(**payload)
        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.data['id'], int(self.client.session.get(
            '_auth_user_id')))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_fails_with_invalid_credentials(self):
        """Test that user login fails with invalid credentials"""

        create_user(email='jv@email.com', password='test123')
        payload = {
            'email': 'jv@email.com',
            'password': 'wrong'
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users request profile
        info"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserApiTests(TestCase):
    """Test APIs requests that require authentication"""

    def setUp(self):
        self.user = create_user(name='jose', password='senha123',
                                email='jvss@email.com.br')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve profile for logged in user"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.user.name)
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        """Test a post is not allowed on the ME URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating profile for authenticated user"""
        payload = {
            'name': 'new_name',
            'password': 'new_pass'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
