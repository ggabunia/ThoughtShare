from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    phone = models.CharField(max_length = 20,  blank = True)
    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length = 264, unique = True )
    priority = models.IntegerField(default=1)
    def __str__(self):
        return self.category_name

class Idea(models.Model):
    def __str__(self):
        return self.i_title
    i_title = models.CharField(max_length = 264, unique = False)
    i_description = models.TextField()
    i_creator = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='seller')
    i_buyer = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, related_name='buyer', blank=True, null=True )
    i_category = models.ForeignKey('Category', on_delete=models.PROTECT)
    i_date_added = models.DateTimeField(auto_now_add = True)
    i_price = models.DecimalField(max_digits=9, decimal_places=2)
    i_likes = models.IntegerField(default=0)
    i_dislikes = models.IntegerField(default=0)
    i_file = models.FileField(upload_to = 'idea_files',blank = True)
    i_date_sold = models.DateTimeField(blank = True, null = True)
    i_is_active = models.BooleanField(default=True)
    i_is_auction = models.BooleanField(default=False)
    i_auction_end = models.DateTimeField(blank = True, null = True)
