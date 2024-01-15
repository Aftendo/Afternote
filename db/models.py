from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    fsid = models.CharField(max_length=16, null=True, unique=True, blank=True)
    mac = models.CharField(max_length=12, null=True, unique=True, blank=True)
    ban = models.BooleanField(default=False, null=False)
    green_star = models.IntegerField(blank=False, null=False, default=0)
    red_star = models.IntegerField(blank=False, null=False, default=0)
    blue_star = models.IntegerField(blank=False, null=False, default=0)
    purple_star = models.IntegerField(blank=False, null=False, default=0)
    def __str__(self):
        return self.username

class Session(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    token = models.CharField(max_length=16, null=False, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    temp = models.CharField(max_length=400, null=False, default="")
    fsid = models.CharField(max_length=16, null=False)
    mac = models.CharField(max_length=12, null=False)
    def __str__(self):
        return "Session "+self.token

class Category(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    internal_id = models.CharField(max_length=16, null=False)
    name = models.CharField(max_length=32, null=False)
    def __str__(self):
        return self.name

class Channel(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    internal_id = models.CharField(max_length=16, null=False)
    name = models.CharField(max_length=32, null=False)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    show_in_frontpage = models.BooleanField(null=False, default=True)
    locked = models.BooleanField(null=False, default=False)
    def __str__(self):
        return self.name

class Flipnote(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    real_filename = models.CharField(max_length=24, null=False, unique=True)
    views = models.IntegerField(null=False, default=0)
    saved = models.IntegerField(null=False, default=0)
    is_locked = models.IntegerField(null=False, default=0)
    made_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=False, on_delete=models.CASCADE)
    star = models.IntegerField(blank=False, null=False, default=0)
    green_star = models.IntegerField(blank=False, null=False, default=0)
    red_star = models.IntegerField(blank=False, null=False, default=0)
    blue_star = models.IntegerField(blank=False, null=False, default=0)
    purple_star = models.IntegerField(blank=False, null=False, default=0)
    total = models.IntegerField(blank=False, null=False, default=0)
    date = models.DateField(auto_now_add=True, null=False)
    def __str__(self):
        return self.real_filename
    
class StarLog(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    flipnote = models.ForeignKey(Flipnote, null=True, on_delete=models.CASCADE)
    star = models.IntegerField(blank=False, null=False, default=0)
    green_star = models.IntegerField(blank=False, null=False, default=0)
    red_star = models.IntegerField(blank=False, null=False, default=0)
    blue_star = models.IntegerField(blank=False, null=False, default=0)
    purple_star = models.IntegerField(blank=False, null=False, default=0)
    def __str__(self):
        return "Star log of "+self.user.username+" for flipnote "+self.flipnote.real_filename