"""
standart django-forms
"""
from django import forms


class AddForm(forms.Form):
    """
    Adding user form
    """
    name = forms.CharField(max_length=100)


class ChangeKillsForm(forms.Form):
    """
    Changing kills form
    """
    name = forms.CharField(max_length=100)
    kills = forms.CharField(max_length=100)


class ChangeWinsForm(forms.Form):
    """
    Changing wins form
    """
    name = forms.CharField(max_length=100)
    wins = forms.CharField(max_length=100)
