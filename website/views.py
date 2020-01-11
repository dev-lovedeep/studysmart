from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.


def homeview(request):

    if request.method == "POST":
        form = request.POST
        userinput = form.get("userinput")
        if userinput != "":
            User_request.objects.create(user_input=userinput)
        return redirect('home')
    else:
        querylist_notice = Notice.objects.all()
        querylist_activity = Activity.objects.all()
        querylist_product = Product.objects.all()
        context = {
            'notice': querylist_notice,
            'activity': querylist_activity,
            'products': querylist_product
        }
        return render(request, "templates/index.html", context)


def productview(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        Product.objects.create(
            itemname=request.POST.get('itemname'),
            price=request.POST.get('price'),
            sellername=request.POST.get('sellername'),
            contact=request.POST.get('contact'),
            imagesrc=uploaded_file_url
        )
        return redirect('buysell')
    else:
        context = {
            "products": Product.objects.all()
        }
        return render(request, 'templates/product.html', context)


def simple_upload(request):
    return render(request, "templates/upload.html", {})


def download_view(request, name):
    if ("books" in request.path):
        download_type = "books and notes"
    else:
        download_type = "paper"

    subject_name = subject_names.objects.get(name=name)

    object_list = download.objects.filter(
        subject=subject_name, category=download_type)

    context = {
        "object": object_list
    }

    return render(request, "templates/download.html", context)


def subject_view(request):
    name = ""
    if ("books" in request.path):
        name = "books and notes"
    if ("paper" in request.path):
        name = "previous year paper"

    context = {
        "pageurl": request.path,
        "pagename": name,
        "objects": subject_names.objects.all()
    }
    return render(request, "templates/subject.html", context)
