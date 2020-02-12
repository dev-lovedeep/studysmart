import glob
import os
import boto3
# from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import *

# drive
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive


# Create your views here.

# view for home page

# check for mimetype
# def file_path_mime(file_path):
#     mime = magic.from_file(file_path, mime=True)
#     return mime


def spacetounderscore(inputurl, filetype):
    url = str(inputurl)
    url = url.replace(' ', '_')
    return "https://studysmartbucket.s3.amazonaws.com/media/{}/{}".format(filetype, url)


# def s3download(request):
#     s3 = boto3.client('s3')
#     s3.download_file('studysmartbucket',
#                      'media/q.png', 'studysmartdownload.png')
#     return redirect("home")


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
    if request.user.is_superuser:
        context = {
            "products": Product.objects.all()
        }
        return render(request, 'templates/filter.html', context)
    else:
        return HttpResponse("you are not allowed to access this url\n<a href='../admin' target='_blank'>login as admin</a>")


def product_delete(request, id):
    if request.user.is_superuser:
        Product.objects.get(id=id).delete()
        return redirect('website:filter')
    else:
        return HttpResponse("you are not allowed to access this url\n<a href='../admin' target='_blank'>login as admin</a>")


def product_approve(request, id):
    if request.user.is_superuser:
        item = Product.objects.get(id=id)
        item.isapproved = "True"
        item.save()
        return redirect('website:filter')

    else:
        return HttpResponse("you are not allowed to access this url\n<a href='../admin' target='_blank'>login as admin</a>")


# display all product to sell


def productview(request):
    context = {
        "products": Product.objects.filter(isapproved=True)
    }
    return render(request, 'templates/product.html', context)

# manage upload product


# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         # print(file_path_mime(os.path.realpath(myfile.name)))
#         product = Product(
#             itemname=request.POST.get('itemname'),
#             price=request.POST.get('price'),
#             sellername=request.POST.get('sellername'),
#             contact=request.POST.get('contact'),
#             uploaded_file=myfile
#         )
#         print(product.uploaded_file.url)
#         product.imagesrc = spacetounderscore(product.uploaded_file.url)
#         product.save()
#         return redirect('home')
#     else:
#         return render(request, "templates/upload.html", {})

def product_upload_view(request):
    newproduct = product_upload_form()
    if request.method == "POST":
        newproduct = product_upload_form(request.POST, request.FILES)

        if newproduct.is_valid():

            notsaved = newproduct.save(commit=False)
            imageurl = spacetounderscore(
                newproduct.cleaned_data.get("uploaded_file"), "images")
            print(imageurl)
            notsaved.imagesrc = imageurl
            # print("url source:"newproduct.imagesrc)
            notsaved.save()
            newproduct = product_upload_form()
            return redirect('home')
    context = {
        "form": newproduct
    }
    return render(request, "templates/upload.html", context)


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


def admin_upload_view(request):
    if request.user.is_superuser:
        pdfurl = ""
        newupload = admin_upload_form()
        if request.method == 'POST':
            # file = request.FILES['file']
            # filename = request.POST.get('filename')
            # subject = request.POST.get('subject', None)
            # download_type = request.POST.get('type', None)
            # linkname = spacetounderscore(file.name)
            # # url = "https://studysmartbucket.s3.amazonaws.com/pdf/{}/{}".format(
            # #     download_type, linkname)
            # url = "https://studysmartbucket.s3.us-east-2.amazonaws.com/media/{}".format(
            #     linkname)
            # # print(subject_names.objects.get(name=subject))
            # download_object = download(
            #     name=filename,
            #     url=url,
            #     subject=subject_names.objects.get(name=subject),
            #     category=download_type,
            #     uploaded_file=file
            # )

            # # url = str(download_object.uplo.url)
            # # url = url.replace('%20', '_')
            # # print("url=", url, "\n\n\n")
            # # product.imagesrc = url
            # # download_object.url=
            # if request.POST.is_valid():
            #     download_object.save()
            #     print("download url:"+url)
            # else:
            #     raise forms.ValidationError("wrong input")
            newupload = admin_upload_form(request.POST, request.FILES)
            print(newupload)
            if newupload.is_valid():
                notsaved = newupload.save(commit=False)
                pdfurl = spacetounderscore(
                    newupload.cleaned_data.get("uploaded_file"), "pdf")
                print(pdfurl)
                notsaved.url = pdfurl
                # print("url source:"newproduct.imagesrc)
                notsaved.save()
                newupload = admin_upload_form()
        context = {
            "form": newupload,
            "subject_list": subject_names.objects.all(),
            "url": pdfurl
        }
        return render(request, 'templates/adminupload.html', context)
    else:
        return HttpResponse("you are not allowed to access this url\n<a href='../admin' target='_blank'>login as admin</a>")


# def setcontent_view(request):
#     print("starting authentication")
#     gauth = GoogleAuth()
#     drive = GoogleDrive(gauth)
#     # this object will allow to access subject drive id of each subjectt
#     subject_list = subject_names.objects.all()
#     # deleting all previous item to prevent override
#     download.objects.all().delete()
#     # started action on each subject
#     for subject in subject_list:
#         # this will fetch the folders in subject folder
#         childfolder = drive.ListFile(
#             {"q": "'{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(subject.driveid)}).GetList()

#         # to create books objects
#         bookid = childfolder[1].get('id')
#         # fetch all items from books folder
#         book_list = drive.ListFile(
#             {'q': "'{}' in parents".format(bookid)}).GetList()

#         for book in book_list:
#             download.objects.create(
#                 name=book['title'], url=book['alternateLink'], subject=subject_names.objects.get(name=subject))

#         # to create paper objects
#         paperid = childfolder[0].get('id')
#         # fetch all the items from paper folder
#         paper_list = drive.ListFile(
#             {'q': "'{}' in parents".format(paperid)}).GetList()
#         for paper in paper_list:
#             download.objects.create(
#                 name=paper['title'], url=paper['alternateLink'], subject=subject_names.objects.get(name=subject), category='paper')

#     print("all links set")
#     return redirect('home')
