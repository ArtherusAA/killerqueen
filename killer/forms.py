from django import forms


class AddForm(forms.Form):
    name = forms.CharField(max_length=100)


class ChangeKillsForm(forms.Form):
    name = forms.CharField(max_length=100)
    kills = forms.CharField(max_length=100)


class ChangeWinsForm(forms.Form):
    name = forms.CharField(max_length=100)
    wins = forms.CharField(max_length=100)