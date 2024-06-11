from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, QuoteForm
from .models import Quote, Author
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import json
# Create your views here.

def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/index.html', {'page_obj': page_obj})


def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quoteapp:add_quote')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})

def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quoteapp:main')
        else:
            return render(request, 'quoteapp/add_quote.html', {'form': form})

    return render(request, 'quoteapp/add_quote.html', {'form': QuoteForm()})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {'author': author})

def scrap_all(request):
    authors = Author.objects.all()
    data = []
    for author in authors:
        author_data={
            'name': author.name,
            'biography': author.biography,
            'quote': []
        }
        quotes = Quote.objects.filter(author=author)
        for quote in quotes:
            author_data['quote'].append({
                'text': quote.text,
            })
        data.append(author_data)
    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=authors_and_quotes.json'
    return response