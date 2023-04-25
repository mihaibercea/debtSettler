from django import forms
from home.models import SessionMember

class InviteForm(forms.Form):

    user = forms.CharField(label='User', max_length=100)

class ZeroSumForm(forms.ModelForm):

    class Meta:
        model = SessionMember
        fields = ['debit', 'parent_session']
        widgets = {
            'parent_session': forms.HiddenInput(attrs={'style': 'display:none;'}),
        }

class SessionForm(forms.Form):
    
    type_choices = (
        ('z', 'Zero Sum'), # zero sum calculates a zero sum between all members. The ballance should always reach 0. 
        ('s', 'Split Sum') # split sum splits debt for all involved members.
    )

    name = forms.CharField()    
    type = forms.ChoiceField(label='Type', choices = type_choices )


class DebitForm(forms.Form):

    debit = forms.FloatField(label = 'Debit')
