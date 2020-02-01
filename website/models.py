from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class Notice(models.Model):
    name = models.CharField(max_length=80)
    src = models.CharField(max_length=120)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=60)
    src = models.CharField(max_length=120)

    def __str__(self):
        return self.name

# model to store user input from "tell us" fiels of home page


class User_request(models.Model):
    user_input = models.CharField(max_length=80)

    def __str__(self):
        return self.user_input


class Product(models.Model):
    itemname = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imagesrc = models.CharField(max_length=120)
    sellername = models.CharField(max_length=20)
    contact = models.BigIntegerField()
    isapproved = models.BooleanField(default=False)
    uploaded_file = models.FileField(blank=True)

    def __str__(self):
        return self.itemname


class subject_names(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


choice = (
    ('books and notes', 'books and notes'),
    ('paper', 'paper')
)


class download(models.Model):
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=120)
    subject = models.ForeignKey(subject_names, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=80, choices=choice, default="books and notes")
    uploaded_file = models.FileField(default="test", validators=[
                                     FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.name
