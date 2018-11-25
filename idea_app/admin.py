from django.contrib import admin
from idea_app import models
# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Idea)
admin.site.register(models.UserProfile)
