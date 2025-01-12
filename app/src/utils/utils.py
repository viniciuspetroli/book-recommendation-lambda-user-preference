import json

def create_gemini_payload(preferred_books):
    book_titles = [book['book_name'] for book in preferred_books]
    content = {}
    return {
        'content': [{
            "parts": [{"text": content}]
        }]
    }

def format_gemini_responde(payload):
    books = []
    for recommendation in response['contents'][0]['parts']:
        books_info = {
            'book_name': recommendation['text'],
            'book_author': recommendation['author'],
            'book_genre': recommendation['genre']
        }
        books.append(books_info)
    return books