from django.db import models

from languages.fields import LanguageField


class Book(models.Model):
    CHOICES = [(y,y) for y in reversed(range(1450, 2021))]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pub_year = models.IntegerField(choices=CHOICES)
    isbn = models.DecimalField(max_digits=13, decimal_places=0)
    num_pages = models.PositiveSmallIntegerField()
    cover_link = models.URLField()
    language = LanguageField(max_length=20)

    def __str__(self):
        return str(self.pub_year) + ' || ' + str(self.title) + ' || ' + str(self.author)
