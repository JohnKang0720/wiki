from django.db import models
from django import forms
# Create your models here.
class WikiPageForm(forms.Form):
    title = forms.CharField(label="Add Title")
    content = forms.CharField(label="Add Content", max_length=10000, widget=forms.TextInput(attrs={'size':80}))