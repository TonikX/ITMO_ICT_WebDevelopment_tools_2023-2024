from rest_framework import serializers
from .models import *


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'


class BooksMemberSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class BookTakingSerializer(serializers.ModelSerializer):
    book = BooksSerializer()
    member = MemberSerializer()

    class Meta:
        model = BookTaking
        fields = '__all__'


class NormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTaking
        fields = '__all__'
