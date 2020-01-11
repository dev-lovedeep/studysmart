from django.contrib import admin
from .models import *

# Register your models here.

# add any new model to this list and it will be automatically registered
mymodels = [Notice, Activity, User_request, Product, download, subject_names]

admin.site.register(mymodels)
