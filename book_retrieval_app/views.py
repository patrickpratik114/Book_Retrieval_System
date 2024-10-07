# book_retrieval_app/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .utils import load_books, create_vector_space_model, search_books
from django.conf import settings
import os

books = load_books()
vectorizer, vector_space_books = create_vector_space_model(books)

def index(request):
    return render(request, 'book_retrieval_app/index.html')

def search(request):
    query = request.GET.get('query', '')
    results = search_books(query, vectorizer, vector_space_books)
    return render(request, 'book_retrieval_app/results.html', {'results': results, 'query': query})

def view_document(request, title):
    book_path = os.path.join(settings.BOOKS_DIR, f"{title}.txt")
    try:
        with open(book_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(book_path, 'r', encoding='iso-8859-1') as file:
            content = file.read()
    return render(request, 'book_retrieval_app/document.html', {'title': title, 'content': content})