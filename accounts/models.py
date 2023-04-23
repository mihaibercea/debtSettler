
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    clubs = models.ManyToManyField('home.Club', help_text='Clubs this user is associated with')

    invites_sent = models.ManyToManyField('home.Invite', help_text='Invites sent by this user', related_name='invites_sent')

    invites_received = models.ManyToManyField('home.Invite', help_text='Invites received by this user', related_name='invites_received')

    #sums = models.ManyToManyField('home.Sum', help_text='Sums assinged to this user')

    # add additional fields in here

    def __str__(self):
        return self.username