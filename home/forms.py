from django import forms
from home.models import SessionMember
from django.utils import timezone

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

    name = forms.CharField(initial=str(timezone.now().date()))    
    type = forms.ChoiceField(label='Type', choices = type_choices )

class LiveSessionForm(forms.Form):
    
    stakes_choices = (
        ('1/2', '1/2'),
        ('1/3', '1/3'),
        ('2/5', '2/5'),
        ('5/10', '5/10'),
        ('5/5', '5/5'),
        ('5/10', '5/10'),
        ('10/10', '10/10'),
        ('10/20', '10/20'),
        ('10/25', '10/25'),
        ('25/50', '25/50'),
        ('50/100', '50/100'),
        ('100/100', '100/100'),
        ('Other', 'Other'),
    )

    game_choices = (        
        ('NLHE', 'NLHE'),
        ('PLO4', 'PLO4'),
        ('PLO5', 'PLO5'),
        ('Pinapple', ' Pineapple'),
        ('Stud', 'Stud'),
        ('HORSE', 'HORSE'),
        ('Other', 'Other')    
    )

    casino = forms.CharField(label='Casino', initial='Casino')    
    stakes = forms.ChoiceField(label='Stakes', choices = stakes_choices )
    game = forms.ChoiceField(label='Game', choices = game_choices )


class DebitForm(forms.Form):

    debit = forms.FloatField(label = 'Final Debit')

class PluslDebit(forms.Form):

    plus_debit = forms.FloatField(label = 'Add more Debit')
