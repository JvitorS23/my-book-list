from books import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('books', views.BooksViewset, basename='books')
router.register('book-gender', views.BookGenderViewSet, basename='book-gender')

app_name = 'books'

urlpatterns = [
    path('', include(router.urls)),
]
