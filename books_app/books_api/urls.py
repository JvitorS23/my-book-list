from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books_api import views

router = DefaultRouter()

router.register('books', views.BooksViewset)
router.register('book-gender', views.BookGenderViewSet)

app_name = 'books_api'

urlpatterns = [
    path('', include(router.urls)),
]