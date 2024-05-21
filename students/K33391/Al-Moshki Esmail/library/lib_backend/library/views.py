from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView


class BooksListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BooksSerializer(books, many=True)
        print(serializer)

        return Response(serializer.data)


class ReservedBooksListView(APIView):
    def get(self, request):
        books = Book.objects.filter(is_lent=True)
        serializer = BooksMemberSerializer(books, many=True)
        print(serializer)

        return Response(serializer.data)


class AvailableBooksListView(APIView):
    def get(self, request):
        books = Book.objects.filter(is_lent=False)
        serializer = BooksSerializer(books, many=True)
        print(serializer)

        return Response(serializer.data)


class MembersListView(APIView):
    def get(self, request):
        books = Member.objects.all()
        serializer = MemberSerializer(books, many=True)
        print(serializer)

        return Response(serializer.data)


class BookTakingListView(APIView):
    def get(self, request):
        books = BookTaking.objects.all()
        serializer = BookTakingSerializer(books, many=True)
        print(serializer)

        return Response(serializer.data)


class CreateBookView(CreateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy('books')


class CreateMemberView(CreateView):
    model = Member
    fields = "__all__"
    success_url = reverse_lazy('members')


class CreateBookTakingView(CreateAPIView):
    serializer_class = NormalSerializer
    success_url = reverse_lazy('bookings')

    def perform_create(self, serializer):
        queryset = BookTaking.objects.none()
        book = serializer.validated_data['book']
        member = serializer.validated_data['member']
        if book.is_lent:
            raise ValidationError("Book is already reserved")

        book.is_lent = True
        book.member = member
        serializer.save()
        book.save()


class DeleteBookTakingView(DestroyAPIView):
    queryset = BookTaking.objects.all()
    serializer_class = BookTakingSerializer
    lookup_field = 'id'
    success_url = reverse_lazy('books')

    def perform_destroy(self, instance):
        book = instance.book
        book.is_lent = False
        book.save()
        instance.delete()
