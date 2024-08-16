from django.db import models
from .myutils import key_gen

# Create your models here.
class User(models.Model):
    img = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    suspended = models.BooleanField(default=True)
    reason = models.CharField(
        max_length=500, blank=True, default="User wasn't given immediate access"
    )
    email = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, default="u")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    unique_key = models.CharField(max_length=100, default=key_gen)
    last_active = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)


class Announcement(models.Model):
    announcer = models.IntegerField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    details = models.CharField(max_length=10000, blank=True)
    added_on = models.DateTimeField(auto_now=True)


class ReadArticle(models.Model):
    obj_id = models.BigIntegerField(primary_key=True, unique=False)
    user_id = models.BigIntegerField(unique=False)
    read_on = models.DateTimeField(auto_now=False, auto_now_add=True)
