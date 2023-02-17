from django import forms

class InviteForm(forms.Form):

    user = forms.CharField(label='User', max_length=100)

class TestForm(forms.Form):

    text = forms.CharField(label='Text', max_length=50)
    