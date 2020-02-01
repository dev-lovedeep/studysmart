from django import forms
from .models import download, Product


class admin_upload_form(forms.ModelForm):
    class Meta:
        model = download
        fields = '__all__'
        exclude = ['url']
    # for checking proper file format

    def clean_uploaded_file(self):
        myfile = self.cleaned_data.get("uploaded_file")
        if not str(myfile).endswith((".pdf")):
            raise forms.ValidationError("invalid format! only pdf allowed")
        return myfile


class product_upload_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['imagesrc', 'isapproved']
    # just for fun :make sure no one can use my name as product

    def clean_itemname(self):
        itemname = self.cleaned_data.get('itemname')
        if 'lovedeep' in itemname:
            raise forms.ValidationError("cannot use admin name")
        return itemname
    # check for contact to be 10 digit no

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if len(str(contact)) != 10:
            raise forms.ValidationError("enter a valid contact no.")
        return contact
    # proper file extension check

    def clean_uploaded_file(self):
        myfile = self.cleaned_data.get("uploaded_file")
        if not str(myfile).endswith((".png", '.jpeg', '.jpg')):
            raise forms.ValidationError("invalid file format")
        if myfile.size > 5242880:  # 5mb
            raise forms.ValidationError("file size should be less than 5MB")
        return myfile
