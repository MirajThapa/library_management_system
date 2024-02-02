from django.urls import path
from .views import (
    create_user,
    list_all_users,
    get_user_by_id,
    add_new_book,
    list_all_books,
    get_book_by_id,
    assign_update_book_details,
    borrow_book,
    return_book,
    list_all_borrowed_books,
)

urlpatterns = [
    # api path for user features
    path('users/', create_user, name='create_user'),
    path('users/all/', list_all_users, name='list_all_users'),
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),

    # api's path for books features
    path('books/', add_new_book, name='add_new_book'),
    path('books/all/', list_all_books, name='list_all_books'),
    path('books/<int:book_id>/', get_book_by_id, name='get_book_by_id'),
    path('books/<int:book_id>/details/', assign_update_book_details, name='assign_update_book_details'),

    # api's for borrowed books
    path('borrowed-books/', borrow_book, name='borrow_book'),
    path('borrowed-books/<int:borrowed_book_id>/return/', return_book, name='return_book'),
    path('borrowed-books/all/', list_all_borrowed_books, name='list_all_borrowed_books'),
]

