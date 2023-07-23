from django.db import models
import uuid # Required for instances
from django.urls import reverse

from django.utils import timezone
import datetime

from accounts.models import CustomUser
from django.db import models


# class ClubMember(CustomUser):
    
#     clubs = models.ManyToManyField

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.username
    
# Create your models here.

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular sum across whole sums list')
    from_member = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, default=None, related_name='from_member')
    to_member = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, default=None, related_name='to_member')    
    parent_session = models.ForeignKey('Session', on_delete = models.CASCADE, default=None)   
    paid = models.BooleanField(default=False)
    time_created = models.DateField(default=timezone.now)
    value = models.FloatField(default=0)

    class Meta:
        ordering = ['id']  

    def __str__(self):
        """String for representing the Model object."""
        return "From " + self.from_user + "to " + self.to_user + "on session " + self.parent_session.name


class Sum(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular sum across whole sums list')
    member = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, default=None)
    current_sum = models.FloatField(default=0)
    parent_session = models.ForeignKey('Session', on_delete = models.CASCADE, default=None)    
    paid = models.BooleanField(default=False)
    time_created = models.DateField(default=timezone.now)
    payments = models.ManyToManyField('Payment', help_text='Create payments for this sum')

    class Meta:
        ordering = ['-time_created']  

    def __str__(self):
        """String for representing the Model object."""
        return self.parent_session.name



class Club(models.Model):


    """Model representing a club."""

    time_created = models.DateField(default=timezone.now)

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular club across whole clubs list')

    name = models.CharField(max_length=200, help_text='Enter a club name')

    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, related_name='club_owner')

    members = models.ManyToManyField('accounts.CustomUser', help_text='Add members to this club')

    invites_sent = models.ManyToManyField('Invite')

    #all_club_members = members.all()

    sessions = models.ManyToManyField('Session')

    sums = models.ManyToManyField('Sum')

    join_requests = models.ManyToManyField('JoinRequest')
    
    class Meta:
        ordering = ['-time_created']    
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this club."""
        return reverse('home:club-detail', args=[str(self.id)])    


class Invite(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular invite')

    parent_club = models.ForeignKey('Club', on_delete=models.CASCADE)

    from_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='from_user')

    to_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='to_user')

    time_created = models.DateField(default=timezone.now)

    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_created']


    def __str__(self):
        """String for representing the Model object."""
        text = 'From ' + str(self.from_user)+ 'to ' + str(self.to_user) + ', with ID: ' + str(self.id)
        return text
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this club."""
        return reverse('home:club-detail', args=[str(self.id)])   

class JoinRequest(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular invite')

    parent_club = models.ForeignKey('Club', on_delete=models.CASCADE)
    
    from_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='Join_request_for_user')

    time_created = models.DateField(default=timezone.now)

    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_created']


    def __str__(self):
        """String for representing the Model object."""
        text = 'For club ' + str(self.parent_club)+ 'from ' + str(self.to_user) + ', with ID: ' + str(self.id)
        return text
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this club."""
        return reverse('home:club-detail', args=[str(self.id)])   
    

class Session(models.Model):

    time_created = models.DateField(default=datetime.date(2000, 1, 1) )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular session across whole sessions list')

    name = models.CharField(max_length=200, default = str(time_created))

    members = models.ManyToManyField('SessionMember', help_text='Add members to this session')

    parent_club = models.ForeignKey('Club', on_delete = models.CASCADE, default=None)

    sums = models.ManyToManyField('Sum')

    payments = models.ManyToManyField('Payment')

    bias = models.FloatField(default=0)

    STATUS_ = (
        ('o', 'open'),
        ('c', 'closed')
    )

    TYPE_ = (
        ('z', 'Zero Sum'), # zero sum calculates a zero sum between all members. The ballance should always reach 0. 
        ('s', 'Split Sum') # split sum splits debt for all involved members.
    )

    type =  models.CharField(
        max_length=1,
        choices=TYPE_,
        blank=True,
        default='z',
        help_text='Type of session',
    )

    status =  models.CharField(
        max_length=1,
        choices=STATUS_,
        blank=True,
        default='o',
        help_text='Status of the session',
    )

    class Meta:
        ordering = ['-time_created']
  

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('home:session-detail', args=[str(self.id)])


class SessionMember(models.Model):

    id = models.CharField(max_length=200, primary_key=True)
    name =  models.CharField(max_length=200, default = 'New Member')
    debit = models.FloatField(default=0)
    settled_sum = models.FloatField(default=0)
    parent_session = models.ForeignKey('Session', on_delete = models.CASCADE, default=None)
    main_account = models.ForeignKey('accounts.CustomUser', on_delete = models.CASCADE, default=None, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class StackDelta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular sum')
    date_created = models.DateField(default=timezone.now)
    parent_session = models.ForeignKey('LiveSession', on_delete = models.CASCADE, default=None)
    value = models.FloatField(default=0)


class LiveSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular session across whole sessions list')
    result_sum = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    casino = models.CharField(max_length=200, default = 'Casino name')
    buy_in = models.FloatField(default=0)

    stack_delta = models.ManyToManyField('StackDelta')

    STAKES_ = (
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

    stakes =  models.CharField(
        max_length=30,
        choices=STAKES_,
        blank=True,
        default='1/2',
        help_text='Stakes played',
    )

    GAME_ = (
        ('NLHE', 'NLHE'),
        ('PLO4', 'PLO4'),
        ('PLO5', 'PLO5'),
        ('Pinapple', ' Pineapple'),
        ('Stud', 'Stud'),
        ('HORSE', 'HORSE'),
        ('Other', 'Other')
    )

    game =  models.CharField(
        max_length=30,
        choices=GAME_,
        blank=True,
        default='NLHE',
        help_text='Stakes played',
    )

    STATUS_ = (
        ('o', 'open'),
        ('c', 'closed')
    )

    status =  models.CharField(
        max_length=1,
        choices=STATUS_,
        blank=True,
        default='o',
        help_text='Status of the session',
    )
