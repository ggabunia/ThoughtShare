from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from . import models


class UserForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g johndoe',
            'pattern': '[A-Za-z0-9_]{3,20}',
            'title': 'alphanumeric symbols or underscore between 3 and 20 characters'
        })
    )
    first_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. John',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    last_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. Doe',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    email = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. johndoe@gmail.com',
        }))
    email_repeat = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. johndoe@gmail.com',
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
    }))
    password_repeat = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
    }))
    phone = forms.CharField(max_length = 20, required = False, widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'e.g. 555 555 555 555',
        }))

    def clean(self):
        clean_data = super().clean()
        if clean_data['email']!=clean_data['email_repeat']:
            raise forms.ValidationError("Emails don't match")
        if clean_data['password']!=clean_data['password_repeat']:
            raise forms.ValidationError("Passwords don't match")
