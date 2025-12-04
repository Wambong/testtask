from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.auth import get_user_model

User = get_user_model()



class ItemForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Item
        fields = [
            'name', "category", "body", "brand", 'price', "stock",
            'wholesale_qty', 'discount_percentage', 'image', "tags"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'wholesale_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'Shipping Address', 'rows': 3})
    )
    country = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Country'})
    )
    state = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'State'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Order'))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']




class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
