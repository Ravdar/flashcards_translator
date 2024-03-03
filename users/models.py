from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, default="images/default_pp.jpg", upload_to="images/")

    def __str__(self):
        return self.user.username
# Create your models here.
