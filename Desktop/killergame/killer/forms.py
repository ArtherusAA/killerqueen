from django import forms

class AddForm(forms.Form):
    name = forms.CharField(label='naasdasdme', max_length=100)