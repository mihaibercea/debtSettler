from allauth.account.models import EmailAddress
from accounts.models import CustomUser

def set_username_as_email(request, sociallogin):
    user = sociallogin.user
    if not user.username and user.email:
        # Generate a username from the email address
        username = user.email.split('@')[0]
        # Check for username uniqueness and modify if necessary
        if CustomUser.objects.filter(username=username).exists():
            i = 1
            while CustomUser.objects.filter(username=f"{username}_{i}").exists():
                i += 1
            username = f"{username}_{i}"
        user.username = username
        user.save()

