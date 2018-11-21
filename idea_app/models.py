from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    phone = models.CharField(max_length = 20,  blank = True)


class Category(models.Model):
    category_name = models.CharField(max_length = 264, unique = True )
    priority = models.IntegerField(default=1)
    def __str__(self):
        return self.category_name

class Idea(models.Model):
    title = models.CharField(max_length = 264, unique = False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    date_added = models.DateTimeField(default = datetime.now)
