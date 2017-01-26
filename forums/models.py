from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class forumCategory(models.Model):

    title = models.CharField(max_length = 90)

    def __str__(self):
        return self.title

class forumSubCategory(models.Model):

    idForumCategory = models.ForeignKey(forumCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length = 90)

    def __str__(self):
        return self.title

class user(models.Model):
    username = models.CharField('Username',max_length=16, unique = True)
    userpassword = models.CharField('Password',max_length=128)
    useremail = models.CharField('E-mail',max_length=128)
    userdate = models.DateTimeField('date registered')
    userDob = models.DateTimeField('date of birth')

    def __str__(self):
        return self.username





class forumPost(models.Model):
    forumSubCategory = models.ForeignKey(forumSubCategory, on_delete = models.CASCADE)
    idUser = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length = 90)
    content_text = models.CharField(max_length = 500)
    date_stamp = models.DateTimeField('date published')

    def publish(self):
        self.date_stamp = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class thread(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idForumPost = models.ForeignKey(forumPost, on_delete = models.CASCADE)
    content_text = models.CharField(max_length = 500)
    date_stamp = models.DateTimeField('date posted')

    def publish(self):
        self.date_stamp = timezone.now()
        self.save()

    def __str__(self):
        return self.content_text









