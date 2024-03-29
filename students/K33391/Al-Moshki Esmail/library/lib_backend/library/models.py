from django.db import models


class Member(models.Model):
    PASSPORT = 'passport'
    ID = "ID"
    BIRTH_CERTIFICATE = "Birth Certificate"

    choices = (
        (PASSPORT, PASSPORT),
        (ID, "ID"),
        (BIRTH_CERTIFICATE, 'Birth Certificate')
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    middles_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    documents_serial = models.CharField(max_length=60)
    DocumentType = models.CharField(
        max_length=60, choices=choices, default=PASSPORT)


class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    description = models.CharField(max_length=300, null=True, blank=True)
    is_lent = models.BooleanField(default=False)
    publication_date = models.DateField(null=True, blank=True)
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, null=True, blank=True)


class BookTaking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_of_rent = models.DateTimeField(auto_now_add=True)
    date_of_return = models.DateTimeField(null=True, blank=True)
    book_returned = models.BooleanField(default=False)
    late_hours = models.FloatField(null=True, blank=True)
