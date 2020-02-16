from django import forms
from .models import download, Product, subject_names, choice, Notice, Activity


class admin_upload_form(forms.ModelForm):
    class Meta:
        model = download
        fields = '__all__'
        exclude = ['url']

    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "w100"
        }
    ))

    category = forms.CharField(required=True, widget=forms.Select(
        attrs={
            "class": "w100"
        }, choices=choice
    ))

    subject = forms.ModelChoiceField(
        queryset=subject_names.objects.all(),
        empty_label="select subject",
        widget=forms.Select(attrs={'class': 'w100'})
    )

    uploaded_file = forms.FileField(required=True, widget=forms.FileInput(
        attrs={
            "class": "w100",
            "accept": "application/pdf,application/zip"
        }
    ))
    # for checking proper file format

    def clean_uploaded_file(self):
        myfile = self.cleaned_data.get("uploaded_file")
        if not str(myfile).endswith((".pdf", ".zip")):
            raise forms.ValidationError(
                "invalid format! only pdf  and zip allowed")
        return myfile

# this is going to be a raw form


class notice_upload_form(forms.Form):
    # class Meta:
    #     model = Notice
    #     fields = '__all__'
    #     exclude = ['src']

    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "w100"
        }
    ))

    category = forms.CharField(required=True, widget=forms.Select(
        attrs={
            "class": "w100"
        }, choices=(
            ('Notice', 'Notice'),
            ('Activity', 'Activity')
        )
    ))

    # subject = forms.ModelChoiceField(
    #     queryset=subject_names.objects.all(),
    #     empty_label="select subject",
    #     widget=forms.Select(attrs={'class': 'w100'})
    # )

    uploaded_file = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            "class": "w100",
            "accept": "application/pdf"
        }
    ))
    # for checking proper file format

    def clean_uploaded_file(self):
        myfile = self.cleaned_data.get("uploaded_file")

        if not str(myfile).endswith((".pdf")) and not str(myfile) == 'None':
            raise forms.ValidationError(
                "invalid format! only pdf allowed")
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

    # overriding field
    price = forms.DecimalField(required=True, widget=forms.NumberInput(
        attrs={
            "class": "full",
            "min": "0"
        }
    ))
    contact = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={
            "class": "full",
            "minlength": "10",
            "maxlength": "10",
            "type": "tel"
        }
    ))

    sellername = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "full"
        }
    ))

    itemname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "full"
        }
    ))
    uploaded_file = forms.FileField(required=True, widget=forms.FileInput(
        attrs={
            "class": "full",
            "accept": "image/*"
        }
    ))
