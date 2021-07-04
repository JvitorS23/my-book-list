from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg
from core.models import Book, BookGender
from books.serializers import BookSerializer, BookGenderSerializer

def landing(request):
    """Render the landing page"""
    return render(request, 'landing.html')


def home(request):
    """Render the home page"""
    if not request.user.is_authenticated:
        return redirect('/login')

    books = Book.objects.all().filter(user=request.user).select_related(
        'gender')

    status_count_queryset = books.values('status').annotate(total=Count(
        'status'))
    status_count = {
        'COMPLETED': 0,
        'READING': 0,
        'PLAN_TO_READ': 0,
        'DROPPED': 0
    }
    for item in status_count_queryset:
        status_count[item['status']] = item['total']

    total_read_pages = books.filter(status='COMPLETED').aggregate(Sum(
        'num_pages'))['num_pages__sum']

    if total_read_pages is None:
        total_read_pages = 0

    mean_score = books.filter(status='COMPLETED').aggregate(Avg(
        'score'))['score__avg']
    if mean_score is not None:
        mean_score = "{:.1f}".format(mean_score)
    else:
        mean_score = '---'

    books = BookSerializer(books, many=True).data

    for book in books:
        book['status'] = book['status'].capitalize().replace('_', ' ')
        if book['score'] == None:
            book['score'] = '---'

    book_genders = BookGender.objects.all()
    book_genders = BookGenderSerializer(book_genders, many=True).data

    page_info = {
        'user_books': books,
        'book_genders': book_genders,
        'status_count': status_count,
        'total_read_pages': total_read_pages,
        'mean_score': mean_score,
    }

    return render(request, 'home.html', page_info)


def login(request):
    """Render the login page"""
    if request.user.is_authenticated:
        return redirect('/home')

    return render(request, 'login.html')


def register(request):
    """Render the register page"""
    if request.user.is_authenticated:
        return redirect('/home')

    return render(request, 'register.html')
