# book_retrieval_app/utils.py

import os
from collections import namedtuple
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from django.conf import settings

Book = namedtuple('Book', ['title', 'content', 'vector'])

def load_books():
    books_dir = settings.BOOKS_DIR
    books = []
    for filename in os.listdir(books_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(books_dir, filename)
            try:
                # First, try to read the file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, try with ISO-8859-1 encoding
                with open(file_path, 'r', encoding='iso-8859-1') as file:
                    content = file.read()
            title = os.path.splitext(filename)[0]
            books.append(Book(title=title, content=content, vector=None))
    return books

def create_vector_space_model(books):
    vectorizer = TfidfVectorizer()
    content_list = [book.content for book in books]
    tfidf_matrix = vectorizer.fit_transform(content_list)
    
    vectorized_books = []
    for i, book in enumerate(books):
        vector = tfidf_matrix[i].toarray()[0]
        vectorized_books.append(Book(title=book.title, content=book.content, vector=vector))
    
    return vectorizer, vectorized_books

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (magnitude1 * magnitude2)

def search_books(query, vectorizer, books):
    query_vector = vectorizer.transform([query]).toarray()[0]
    results = []
    for book in books:
        similarity = cosine_similarity(query_vector, book.vector)
        results.append((book, similarity))
    return sorted(results, key=lambda x: x[1], reverse=True)[:5]