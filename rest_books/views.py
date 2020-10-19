import json

import requests
from django.core.exceptions import ValidationError

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import UpdateView, CreateView
from django.views.generic.base import View

from rest_books.forms import CreateBookForm, SearchBookForm
from rest_books.models import Book

from .filters import BookFilter


def filtered_books(request):
    my_filter = BookFilter(request.GET, queryset=Book.objects.all().order_by('id').reverse())
    context = {
        'books': Book.objects.all().order_by('id'),
        'my_filter': my_filter,
    }
    return render(request, 'rest_books/books.html', context)


class CreateBookView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'rest_books/create_book.html'
    field = ['__all__']
    success_url = reverse_lazy('books')


class UpdateBookView(UpdateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'rest_books/update_book.html'
    success_url = '/books'

    def get_object(self):
        object_id = self.kwargs.get("id")
        return get_object_or_404(Book, id=object_id)


class ImportBooks(View):
    form_class = SearchBookForm
    template_name = 'rest_books/import_books.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            key_word = form.cleaned_data['key_word']
            search_result = self.search(key_word)

            if 'title' not in search_result[0]['volumeInfo'].keys():
                search_result_title = 'MISSING!'
            else:
                search_result_title = search_result[0]['volumeInfo']['title']
            if 'authors' not in search_result[0]['volumeInfo'].keys():
                search_result_author = 'MISSING!'
            else:
                for author in search_result[0]['volumeInfo']['authors']:
                    search_result_author = author
            if 'publishedDate' not in search_result[0]['volumeInfo'].keys():
                search_result_pub_year = 'MISSING!'
            else:
                search_result_pub_year = search_result[0]['volumeInfo']['publishedDate'][:4]
            if 'pageCount' not in search_result[0]['volumeInfo'].keys():
                search_result_num_pages = 'MISSING!'
            else:
                search_result_num_pages = search_result[0]['volumeInfo']['pageCount']
            if 'industryIdentifiers' not in search_result[0]['volumeInfo'].keys():
                search_result_id_type = 'MISSING!'
                search_result_id = 'MISSING!'
            elif search_result[0]['volumeInfo']['industryIdentifiers'][0]['type'] == 'OTHER':
                search_result_id_type = 'INCORRECT ID type!' + search_result[0]['volumeInfo']['industryIdentifiers'][0]['type']
                search_result_id = search_result[0]['volumeInfo']['industryIdentifiers'][0]['identifier']
            else:
                search_result_id_type = search_result[0]['volumeInfo']['industryIdentifiers'][0]['type']
                search_result_id = search_result[0]['volumeInfo']['industryIdentifiers'][0]['identifier']

            if 'imageLinks' not in search_result[0]['volumeInfo'].keys():
                search_result_cover_link = 'MISSING!'
            else:
                search_result_cover_link = search_result[0]['volumeInfo']['imageLinks']['smallThumbnail']
            if 'language' not in search_result[0]['volumeInfo'].keys():
                search_result_language = 'MISSING!'
            else:
                search_result_language = search_result[0]['volumeInfo']['language']

            context = {
                'form': form,
                'search_result_title': search_result_title,
                'search_result_author': search_result_author,
                'search_result_pub_year': search_result_pub_year,
                'search_result_id_type': search_result_id_type,
                'search_result_id': search_result_id,
                'search_result_num_pages': search_result_num_pages,
                'search_result_cover_link': search_result_cover_link,
                'search_result_language': search_result_language,
            }

            self.add_to_db(search_result)
            return render(request, self.template_name, context)

    def search(self, value):
        params = {'q': value, 'maxResults': '1', 'printType': 'books'}
        response = requests.get(url="https://www.googleapis.com/books/v1/volumes/", params=params)
        response_json = response.json()
        books_json = response_json.get('items')
        return books_json

    def add_to_db(self, books_json):
        for book in books_json:
            try:
                for author in book['volumeInfo']['authors']:
                    authors = author

                Book.objects.get_or_create(
                    title=book['volumeInfo']['title'],
                    author=authors,
                    pub_year=book['volumeInfo']['publishedDate'][:4],
                    isbn=book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                    num_pages=book['volumeInfo']['pageCount'],
                    cover_link=book['volumeInfo']['imageLinks']['smallThumbnail'],
                    language=book['volumeInfo']['language'],
                )

            except ValidationError as vaer:
                print("ValidationError:", vaer)
            except TypeError as tyer:
                print("TypeError:", tyer)
            except KeyError as kyer:
                print("KeyError:", kyer)
