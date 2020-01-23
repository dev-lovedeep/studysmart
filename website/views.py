import glob
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Create your views here.

# view for home page
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


# show non approved products
def product_filter(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, 'templates/filter.html', context)


def product_delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect('website:filter')


def product_approve(request, id):
    item = Product.objects.get(id=id)
    print(item.isapproved)
    item.isapproved = "True"
    item.save()
    print(item.isapproved)
    return redirect('website:filter')

# display all product to sell


def productview(request):
    context = {
        "products": Product.objects.filter(isapproved=True)
    }
    return render(request, 'templates/product.html', context)

# manage upload product


def simple_upload(request):
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
        return render(request, "templates/upload.html", {})

# supply item to set on both paper and books page


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

# manage the list of subject and next page to direct


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

# contact page view


def contact_view(request):
    return render(request, 'templates/Contact.html', {})

# set all the links from google drive


def setcontent_view(request):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    # this object will allow to access subject drive id of each subjectt
    subject_list = subject_names.objects.all()
    # deleting all previous item to prevent override
    download.objects.all().delete()
    # started action on each subject
    for subject in subject_list:
        # this will fetch the folders in subject folder
        childfolder = drive.ListFile(
            {"q": "'{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(subject.driveid)}).GetList()

        # to create books objects
        bookid = childfolder[1].get('id')
        # fetch all items from books folder
        book_list = drive.ListFile(
            {'q': "'{}' in parents".format(bookid)}).GetList()

        for book in book_list:
            download.objects.create(
                name=book['title'], url=book['alternateLink'], subject=subject_names.objects.get(name=subject))

        # to create paper objects
        paperid = childfolder[0].get('id')
        # fetch all the items from paper folder
        paper_list = drive.ListFile(
            {'q': "'{}' in parents".format(paperid)}).GetList()
        for paper in paper_list:
            download.objects.create(
                name=paper['title'], url=paper['alternateLink'], subject=subject_names.objects.get(name=subject), category='paper')
    return redirect('home')
