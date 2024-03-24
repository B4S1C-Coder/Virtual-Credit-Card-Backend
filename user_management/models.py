from django.db import models
from django.contrib.auth.models import User

class AdditionalUserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, default="Nothing to see here ...")
    phone_no = models.CharField(max_length=10)
    status = models.BooleanField('status', default=True)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True,
					default='user_avatars/default_user.png')
