from django import forms

class InviteForm(forms.Form):

    user = forms.CharField(label='User', max_length=100)