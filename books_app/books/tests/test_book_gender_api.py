from books.serializers import BookGenderSerializer
from core.models import BookGender
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


BOOKGENDER_URL = reverse('books:book-gender-list')


def detail_url(book_gender_id):
    """Return book detail URL"""
    return reverse('books:book-gender-detail', args=[book_gender_id])


def create_book_gender(**params):
    """Create sample book gender"""
    return BookGender.objects.create(**params)


class PublicBookGenderApiTests(TestCase):
    """Test the books gender API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(BOOKGENDER_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBookGenderApiTests(TestCase):
    """Test the books gender API (private) features for the normal user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test_password'
        )

        self.user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'test_password'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_owned_book_genders(self):
        """Test retrieving a list of book genders"""
        create_book_gender(name='Action', user=self.user)
        create_book_gender(name='Drama', user=self.user2)

        res = self.client.get(BOOKGENDER_URL)
        book_genders = BookGender.objects.all().filter(user=self.user)
        serializer = BookGenderSerializer(book_genders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_gender_detail(self):
        """Test retrieving a specific book gender"""
        book_gender = create_book_gender(name='Action', user=self.user)

        url = detail_url(book_gender.id)

        res = self.client.get(url)

        serializer = BookGenderSerializer(book_gender, many=False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_other_user_book_gender_detail_fails(self):
        """Test retrieving other user book gender fails"""
        book_gender = create_book_gender(name='Fantasy', user=self.user2)
        url = detail_url(book_gender.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_gender(self):
        """Test that a super user can create a book gender """
        payload = {
            'name': 'Drama'
        }

        res = self.client.post(BOOKGENDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_edit_book_gender(self):
        """Test that a user can edit a book gender """
        book_gender = create_book_gender(name='Action', user=self.user)

        url = detail_url(book_gender.id)
        payload = {
            'name': 'Drama'
        }

        res = self.client.put(url, payload)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cannot_edit_other_users_book_genders(self):
        """Test that a user cannot edit other user book genders """
        book_gender = create_book_gender(name='Action', user=self.user2)

        url = detail_url(book_gender.id)
        payload = {
            'name': 'Drama'
        }

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
