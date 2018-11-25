from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from . import models


class UserForm(forms.Form):
    form_username = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Username...',
            'pattern': '[A-Za-z0-9_]{3,20}',
            'title': 'alphanumeric symbols or underscore between 3 and 20 characters'
        })
    )
    form_first_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-first-name form-control',
            'id' : 'form-first-name',
            'placeholder' : 'First name...',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    form_last_name = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-last-name form-control',
            'id' : 'form-last-name',
            'placeholder' : 'Last name...',
            'pattern': '([^\s][A-zÀ-ž\s]+)',
            'title': 'Alphabet symbols and spaces only'
        }))
    form_email = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-email form-control',
            'placeholder' : 'Email...',
            'id' :'form-email',
        }))
    form_email_repeat = forms.EmailField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-email form-control',
            'placeholder' : 'Repeat Email...',
            'id' :'form-email-repeat',
        }))
    form_password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-password form-control',
        'placeholder':'Password...',
        'id' : 'form-password',
    }))
    form_password_repeat = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-password form-control',
        'placeholder':'Repeat Password...',
        'id' : 'form-password-repeat',
    }))
    form_phoneNumber = forms.CharField(max_length = 20, required = False, widget = forms.TextInput(
        attrs = {
            'class' : 'form-phoneNumber form-control',
            'placeholder' : 'Phone Number...',
            'id':'form-phoneNumber',
        }))

    def clean(self):
        clean_data = super().clean()
        if clean_data['form_email']!=clean_data['form_email_repeat']:
            raise forms.ValidationError("Emails don't match")
        if clean_data['form_password']!=clean_data['form_password_repeat']:
            raise forms.ValidationError("Passwords don't match")


class IdeaForm(forms.ModelForm):
    class Meta:
        model = models.Idea
        fields = ['i_title','i_description','i_category','i_price',]
