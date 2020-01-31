from django.urls import path
from website.views import product_filter, product_delete, product_approve, admin_upload_view

app_name = "website"
urlpatterns = [

    # path('set', setcontent_view, name="set"),  # insert new record
    path('approve', product_filter, name="filter"),
    # path('download', s3download, name="s3download"),
    path('upload', admin_upload_view, name="adminupload"),
    path('approve/<int:id>/approve', product_approve, name="approve"),
    path('approve/<int:id>/delete', product_delete, name="remove"),

]
