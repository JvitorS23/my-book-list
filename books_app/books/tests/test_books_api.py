from books.serializers import BookSerializer
from core.models import Book, BookGender
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

BOOKS_URL = reverse('books:books-list')


def detail_url(book_id):
    """Return book detail URL"""
    return reverse('books:books-detail', args=[book_id])


def create_book(**params):
    """Create sample book"""
    return Book.objects.create(**params)


def create_book_gender(**params):
    """Create sample book gender"""
    return BookGender.objects.create(**params)


class PublicBooksApiTests(TestCase):
    """Test the books API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBooksApiTests(TestCase):
    """Test the books API (private) """

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

    def test_retrieve_books(self):
        """Test retrieving a list of books"""
        create_book(user=self.user, title='A', author='Jv', num_pages=123,
                    status='COMPLETED', score=7)
        create_book(user=self.user, title='B', author='Jv', num_pages=123,
                    status='COMPLETED', score=7)

        res = self.client.get(BOOKS_URL)
        books = Book.objects.all().order_by('-id')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_valid_payload_success(self):
        """Test creating creating a book with valid payload is successful"""
        payload = {
            'title': 'Harry Potter',
            'author': 'jv',
            'num_pages': 123,
            'status': 'COMPLETED',
            'score': 8,
        }

        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Book.objects.all().filter(
            id=res.data['id']).exists()
        self.assertTrue(exists)

    def test_create_book_invalid_payload_fails(self):
        """Test creating creating a book with invalid payload fails"""
        # No title
        payload = {
            'author': 'jv',
            'num_pages': 123,
            'status': 'COMPLETED',
            'score': 8,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid num pages
        payload = {
            'author': 'jv',
            'title': 'HP',
            'num_pages': -1,
            'status': 'COMPLETED',
            'score': 8,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid score
        payload = {
            'author': 'jv',
            'title': 'HP',
            'num_pages': 100,
            'status': 'COMPLETED',
            'score': -1,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid status
        payload = {
            'author': 'jv',
            'title': 'HP',
            'num_pages': 100,
            'status': 'sadsad',
            'score': 10,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid gender
        payload = {
            'author': 'jv',
            'title': 'HP',
            'num_pages': 100,
            'status': 'COMPLETED',
            'score': 1,
            'gender': 2,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # no author
        payload = {
            'title': 'HP',
            'num_pages': 100,
            'status': 'COMPLETED',
            'score': 1,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_gender(self):
        """Test creating a book with a gender"""
        sample_gender = create_book_gender(name='Drama', user=self.user)
        payload = {
            'title': 'Harry Potter',
            'author': 'jv',
            'num_pages': 123,
            'status': 'COMPLETED',
            'score': 8,
            'gender': sample_gender.id
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Book.objects.all().filter(
            id=res.data['id']).exists()
        self.assertTrue(exists)

    def test_full_update_book(self):
        """Test if update endpoint works"""
        gender = create_book_gender(name='Drama', user=self.user)
        book = create_book(user=self.user, author='jose', title='B',
                           num_pages=123, status='COMPLETED', score=7,
                           gender=gender)

        new_gender = create_book_gender(name='Ação', user=self.user)
        payload = {
            'title': 'Update title',
            'author': 'jv',
            'num_pages': 25,
            'status': "DROPPED",
            'score': 10,
            'gender': new_gender.id
        }

        url = detail_url(book.id)
        self.client.put(url, payload)
        book.refresh_from_db()

        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.author, payload['author'])
        self.assertEqual(book.num_pages, payload['num_pages'])
        self.assertEqual(book.status, payload['status'])
        self.assertEqual(book.score, payload['score'])
        self.assertEqual(book.gender.id, payload['gender'])

    def test_partial_update_book(self):
        """Test if update endpoint works"""
        gender = create_book_gender(name='Drama', user=self.user)
        book = create_book(user=self.user, author='jose', title='B',
                           num_pages=123, status='READING', score=7,
                           gender=gender)

        payload = {
            'status': "COMPLETED",
            'score': 10,
        }

        url = detail_url(book.id)
        self.client.patch(url, payload)
        book.refresh_from_db()

        self.assertEqual(book.status, payload['status'])
        self.assertEqual(book.score, payload['score'])

    def test_user_only_access_owned_books(self):
        """Test if user can access only the owned objects"""
        create_book(user=self.user2, author='jose', title='B',
                    num_pages=123, status='READING', score=7)

        create_book(user=self.user, author='jose', title='B',
                    num_pages=123, status='READING', score=7)

        res = self.client.get(BOOKS_URL)
        books = Book.objects.all().filter(user=self.user)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_filter_books_by_status(self):
        """Test filtering books by status"""
        book1 = create_book(user=self.user, author='jose', title='A',
                            num_pages=123, status='READING', score=7)

        book2 = create_book(user=self.user, author='jose', title='B',
                            num_pages=123, status='COMPLETED', score=7)

        res = self.client.get(
            BOOKS_URL,
            {'status': 'READING'}
        )

        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filter_books_by_gender(self):
        """Test filtering books by gender"""
        gender1 = create_book_gender(name='Drama', user=self.user)
        book1 = create_book(user=self.user, author='jose', title='A',
                            num_pages=123, status='READING', score=7,
                            gender=gender1)

        gender2 = create_book_gender(name='Fantasia', user=self.user)
        book2 = create_book(user=self.user, author='jose', title='B',
                            num_pages=123, status='COMPLETED', score=7,
                            gender=gender2)

        res = self.client.get(
            BOOKS_URL,
            {'gender': gender1.id}
        )

        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
