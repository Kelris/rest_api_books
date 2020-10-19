from unittest import TestCase

from django.test import Client
from django.urls import path, include, resolve

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

from rest_books.models import Book


class BookTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_names(self):
        self.assertEqual(reverse('books'), '/books/')
        self.assertEqual(reverse('update_book', kwargs={'id': 1}), '/books/1')
        self.assertEqual(reverse('import_view'), '/books/import')

        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('update_book', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('import_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_addresses(self):
        url_addresses = [
            'http://testserver/books/',
            'http://testserver/books/1',
            'http://testserver/books/import',
        ]

        for url in url_addresses:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_object(self):
        Book.objects.create(
            title='Lalka',
            author='Bolesław Prus',
            pub_year='1890',
            isbn='5879856241586',
            num_pages='584',
            cover_link='https://ecsmedia.pl/c/lalka-b-iext39898101.jpg',
            language='pl',
        )

        self.assertIn(Book.objects.get(
            title='Lalka',
            author='Bolesław Prus',
            pub_year='1890',
            isbn='5879856241586',
            num_pages='584',
            cover_link='https://ecsmedia.pl/c/lalka-b-iext39898101.jpg',
            language='pl'), Book.objects.all())

    def test_book_import(self):
        self.client.post('http://testserver/books/import', {
            'key_word': 'krew, pot'
        })
        self.assertIn(Book.objects.get(title='Krew, pot i piksele. Chwalebne i niepokojące opowieści o tym, jak robi się gry'), Book.objects.all())


class RestApiTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('rest_books.urls'))
    ]

    def setUp(self):
        client = APIClient()
        client.post('/rest_books/', {
            'title': 'Lalka',
            'author': 'Bolesław Prus',
            'pub_year': '1890',
            'isbn': '5879856241586',
            'num_pages': '584',
            'cover_link': 'https://ecsmedia.pl/c/lalka-b-iext39898101.jpg',
            'language': 'pl',
        }, format='json')

    def test_rest_url_names(self):
        self.assertEqual(reverse('books-list'), '/rest_books/')
        self.assertEqual(reverse('rest_det_upd_del', kwargs={'id': 1}), '/rest_books/1')

        response = self.client.get(reverse('books-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('rest_det_upd_del', kwargs={'id': 1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_addresses(self):
        url_addresses = [
            'http://testserver/rest_books/',
            'http://testserver/rest_books/1',
        ]

        for url in url_addresses:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_object(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Lalka')
        self.assertEqual(Book.objects.get().author, 'Bolesław Prus')
        self.assertEqual(Book.objects.get().pub_year, 1890)
        self.assertEqual(Book.objects.get().isbn, 5879856241586)
        self.assertEqual(Book.objects.get().num_pages, 584)
        self.assertEqual(Book.objects.get().cover_link, 'https://ecsmedia.pl/c/lalka-b-iext39898101.jpg')
        self.assertEqual(Book.objects.get().language, 'pl')

    def test_book_wrong_post(self):
        response = self.client.post('http://testserver/rest_books/', {
            'title': '',
            'author': '',
            'pub_year': '2020',
            'isbn': '',
            'num_pages': '',
            'cover_link': '',
            'language': 'Afar',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': 'X',  # wrong
            'num_pages': '150',
            'cover_link': 'https://api.culture.pl/sites/default/files/images/imported/literatura/okladki/Wiedzmin_/the_witcher_curse_of_crows.jpg',
            'language': 'pl',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': '123456789123499999999999',  # wrong
            'num_pages': '150',
            'cover_link': 'https://api.culture.pl/sites/default/files/images/imported/literatura/okladki/Wiedzmin_/the_witcher_curse_of_crows.jpg',
            'language': 'pl',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': '1234567891234XXXXXXXXXXXXXXX',  # wrong
            'num_pages': '150',
            'cover_link': 'https://api.culture.pl/sites/default/files/images/imported/literatura/okladki/Wiedzmin_/the_witcher_curse_of_crows.jpg',
            'language': 'pl',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': '1234567891234',
            'num_pages': 'X',  # wrong
            'cover_link': 'https://api.culture.pl/sites/default/files/images/imported/literatura/okladki/Wiedzmin_/the_witcher_curse_of_crows.jpg',
            'language': 'pl',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': '1234567891234',
            'num_pages': '150',
            'cover_link': '0',  # wrong
            'language': 'pl',
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)

        response = self.client.post('http://testserver/rest_books/', {
            'title': 'Wiedźmin',
            'author': 'Andrzej Sapkowski',
            'pub_year': '1991',
            'isbn': '1234567891234',
            'num_pages': '150',
            'cover_link': 'https://api.culture.pl/sites/default/files/images/imported/literatura/okladki/Wiedzmin_/the_witcher_curse_of_crows.jpg',
            'language': '0',  # wrong
        }, format='json')
        assert response.status_code == 400
        self.assertEqual(Book.objects.all().count(), 1)
