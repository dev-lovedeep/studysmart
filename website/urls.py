from django.urls import path
from website.views import setcontent_view, product_filter, product_delete, product_approve

app_name = "website"
urlpatterns = [

    path('set', setcontent_view, name="set"),  # insert new record
    path('approve', product_filter, name="filter"),
    path('approve/<int:id>/approve', product_approve, name="approve"),
    path('approve/<int:id>/delete', product_delete, name="remove"),

]
