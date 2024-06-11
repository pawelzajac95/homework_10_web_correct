from django import forms
from .models import Author, Quote

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Author.objects.filter(name=name).exists():
            raise forms.ValidationError("Author with this name already exists.")
        return name

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author']
