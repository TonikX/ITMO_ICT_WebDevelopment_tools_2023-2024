from django.urls import path
from . import views

urlpatterns = [
    path("all-books/", views.BooksListView.as_view()),
    path("books/", views.AvailableBooksListView.as_view(), name='books'),
    path("reserved-books/", views.ReservedBooksListView.as_view()),
    path("members/", views.MembersListView.as_view(), name='members'),
    path("bookings/", views.BookTakingListView.as_view(), name='bookings'),
    path("create-book/", views.CreateBookView.as_view()),
    path("create-member/", views.CreateMemberView.as_view()),
    path('create-booking/', views.CreateBookTakingView.as_view()),
    path("delete-booking/<int:id>", views.DeleteBookTakingView.as_view())
]
