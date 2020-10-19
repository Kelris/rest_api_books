from rest_framework import serializers

from rest_books.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'pub_year', 'isbn', 'num_pages', 'cover_link', 'language']
