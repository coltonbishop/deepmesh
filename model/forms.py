from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import ModelForm

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=250, required=False)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()