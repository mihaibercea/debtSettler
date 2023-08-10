
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    
    clubs = models.ManyToManyField('home.Club', help_text='Clubs this user is associated with')

    invites_sent = models.ManyToManyField('home.Invite', help_text='Invites sent by this user', related_name='invites_sent')

    invites_received = models.ManyToManyField('home.Invite', help_text='Invites received by this user', related_name='invites_received')

    sums = models.ManyToManyField('home.Sum', help_text='Sums assinged to this user')

    payments = models.ManyToManyField('home.payment', help_text='Payments involving this user')

    join_requests = models.ManyToManyField('home.JoinRequest')

    livesessions = models.ManyToManyField('home.LiveSession', help_text='livesessions')

    # add additional fields in here

    def __str__(self):
        return self.username
        
    def save(self, *args, **kwargs):
        if not self.username and self.email:
            # Generate a username from the email address
            self.username = slugify(self.email.split('@')[0])
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['username']    