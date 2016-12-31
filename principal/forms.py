#encoding:utf-8
from django import forms


class SearchForm(forms.Form):
    criteria = forms.CharField(label="Search artists, albums or songs")
