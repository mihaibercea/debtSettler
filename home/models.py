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

class Club(models.Model):


    """Model representing a club."""

    time_created = models.DateField(default=timezone.now)

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular club across whole clubs list')

    name = models.CharField(max_length=200, help_text='Enter a club name')

    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, related_name='club_owner')

    members = models.ManyToManyField('accounts.CustomUser', help_text='Add members to this club')

    #all_club_members = members.all()

    sessions = models.ManyToManyField('Session')
    
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

    club = models.ForeignKey('Club', on_delete=models.CASCADE)

    from_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='from_user')

    to_user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='to_user')

    time_created = models.DateField(default=timezone.now)

    def __str__(self):
        """String for representing the Model object."""
        text = 'From ' + self.from_user + 'to ' + self.to_user + ', with ID: ' + str(self.id)
        return text
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this club."""
        return reverse('home:club-detail', args=[str(self.id)])   
    

class Session(models.Model):

    time_created = models.DateField(default=datetime.date(2000, 1, 1) )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular session across whole sessions list')

    name = models.CharField(max_length=200, default = 'New Session')

    members = models.ManyToManyField('accounts.CustomUser', help_text='Add members to this session')

    #parent_club = models.ForeignKey('Club', on_delete = models.CASCADE, default=Club.objects.get(name='PPC').id)

    STATUS_ = (
        ('o', 'open'),
        ('c', 'closed')
    )

    TYPE_ = (
        ('z', 'Zero Sum'), 
        ('s', 'Split Sum')
    )

    type =  models.CharField(
        max_length=1,
        choices=TYPE_,
        blank=True,
        default='o',
        help_text='Type of session',
    )

    status =  models.CharField(
        max_length=1,
        choices=STATUS_,
        blank=True,
        default='z',
        help_text='Status of the session',
    )

    class Meta:
        ordering = ['-time_created']
  

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('home:session-detail', args=[str(self.id)])
    