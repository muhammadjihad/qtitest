from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserExtend(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    city=models.CharField(max_length=35)
    zipcode=models.CharField(max_length=8)

    def __str__(self):
        return self.user.username