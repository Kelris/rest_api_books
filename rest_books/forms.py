from django import forms

from .models import Book


class CreateBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):                                                                                # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#styling-widget-instances
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
        self.fields['author'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Author'})
        self.fields['pub_year'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Publication year'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ISBN'})
        self.fields['num_pages'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of the pages'})
        self.fields['cover_link'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cover link'})
        self.fields['language'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Language'})


class SearchBookForm(forms.Form):
    key_word = forms.CharField(max_length=100, widget=forms.TextInput({'class': 'form-control', 'placeholder':'Key word'}))
