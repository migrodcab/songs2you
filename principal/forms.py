#encoding:utf-8
from django import forms


class SearchForm(forms.Form):
    criteria = forms.CharField(label="Search artists, albums or songs")
    
class UserForm(forms.Form):
    fields = (('Male','Male'),('Female','Female'))    
    
    username = forms.CharField(max_length=20, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput, label="Repeat Password, please")
    firstName = forms.CharField(max_length=100, label="First name")
    lastName = forms.CharField(max_length=100, label="Last name")
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(fields, label="Gender")
