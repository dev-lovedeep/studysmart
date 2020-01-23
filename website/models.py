from django.db import models


# Create your models here.


class Notice(models.Model):
    name = models.CharField(max_length=80)
    src = models.URLField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=60)
    src = models.URLField()

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
    imagesrc = models.URLField()
    sellername = models.CharField(max_length=20)
    contact = models.BigIntegerField()
    isapproved = models.BooleanField(default=False)

    def __str__(self):
        return self.itemname


class subject_names(models.Model):
    name = models.CharField(max_length=80)
    driveid = models.TextField()

    def __str__(self):
        return self.name


choice = (
    ('books and notes', 'books and notes'),
    ('paper', 'paper')
)


class download(models.Model):
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=80)
    subject = models.ForeignKey(subject_names, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=80, choices=choice, default="books and notes")

    def __str__(self):
        return self.name
