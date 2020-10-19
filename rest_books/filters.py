import django_filters
from django_filters import CharFilter, NumberFilter

from django.forms import TextInput

from .models import Book

class BookFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains', widget=TextInput({'class': 'form-control','placeholder': 'Title contains '}))
    author = CharFilter(field_name="author", lookup_expr='icontains', widget=TextInput({'class': 'form-control','placeholder': 'Author contains '}))
    language = CharFilter(field_name="language", lookup_expr='icontains', widget=TextInput({'class': 'form-control','placeholder': 'Language contains '}))
    start_date = NumberFilter(field_name="pub_year", lookup_expr="gte", widget=TextInput({'class': 'form-control','placeholder': 'From: YYYY'}))
    end_date = NumberFilter(field_name="pub_year", lookup_expr="lte", widget=TextInput({'class': 'form-control','placeholder': 'To: YYYY'}))

    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['pub_year', 'isbn', 'num_pages', 'cover_link']
