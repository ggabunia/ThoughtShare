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
        return self.title
    title = models.CharField(max_length = 264, unique = False)
    description = models.TextField()
    content = models.TextField(blank=True)
    creator = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='seller')
    buyer = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, related_name='buyer', blank=True, null=True )
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add = True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    file = models.FileField(upload_to = 'idea_files',blank = True,null = True)
    date_sold = models.DateTimeField(blank = True, null = True)
    is_public = models.BooleanField(default=True)
    is_auction = models.BooleanField(default=False)
    auction_end = models.DateTimeField(blank = True, null = True)

class IdeaRating(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='rate_giver')
    idea = models.ForeignKey('Idea',on_delete=models.CASCADE, related_name='idea')
    is_positive = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add = True)
    def save(self, *args, **kwargs):
        idea = Idea.objects.get(pk=self.idea.pk)
        if self.is_positive:
            idea.likes+=1
        else:
            idea.dislikes +=1
        idea.save()

        super(IdeaRating, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):

        idea = Idea.objects.get(pk=self.idea.pk)
        if self.is_positive:
            idea.likes -= 1
        else:
            idea.dislikes -= 1
        idea.save()
        super(IdeaRating, self).delete(*args, **kwargs)
