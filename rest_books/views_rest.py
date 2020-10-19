from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters

from rest_books.models import Book
from rest_books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title','title', 'author', 'pub_year', 'isbn', 'num_pages', 'cover_link', 'language']
    filterset_fields = ['title', 'author', 'pub_year', 'isbn', 'num_pages', 'cover_link', 'language']
    ordering_fields = ['title', 'author', 'pub_year', 'language']
    ordering = ['id']


class BookDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = "id"
