from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

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
    username = models.CharField(max_length=16, unique = True)
    userpassword = models.CharField(max_length=128)
    useremail = models.CharField(max_length=128)
    userdate = models.DateTimeField('date registered')
    userDob = models.DateTimeField('date of birth')

    def __str__(self):
        return self.username





class forumPost(models.Model):
    forumSubCategory = models.ForeignKey(forumSubCategory, on_delete = models.CASCADE)
    idUser = models.ForeignKey(user,on_delete=models.CASCADE)
    title = models.CharField(max_length = 90)
    content_text = models.CharField(max_length = 500)
    date_stamp = models.DateTimeField('date published')

    def publish(self):
        self.date_stamp = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class thread(models.Model):
    idUser = models.ForeignKey(user, on_delete=models.CASCADE)
    idForumPost = models.ForeignKey(forumPost, on_delete = models.CASCADE)
    content_text = models.CharField(max_length=500)

    date_stamp = models.DateTimeField('date posted')

    def __str__(self):
        return self.idUser.username











