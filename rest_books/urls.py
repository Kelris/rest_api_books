'''The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')'''

from django.urls import path, include

from rest_framework import routers

from rest_books.views import filtered_books, UpdateBookView, ProcessCreateBook, ImportBooks, CreateBookView
from rest_books.views_rest import BookViewSet, BookDetailUpdateDelete

router = routers.DefaultRouter()
router.register(r'rest_books', BookViewSet, basename='books')


urlpatterns = [
    path('books/', filtered_books, name='books'),
    path('books/import', ImportBooks.as_view(), name='import_view'),
    path('books/create/', CreateBookView.as_view(), name='create_book'),
    path('books/<int:id>', UpdateBookView.as_view(), name='update_book'),

    path('process_creation', ProcessCreateBook.as_view(), name='process_creation'),

    path('', include(router.urls)),
    path('rest_books/<id>', BookDetailUpdateDelete.as_view(), name='rest_det_upd_del')
]
