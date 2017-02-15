from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required



fs = FileSystemStorage(location=settings.USER_IMAGE_PATH)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)

    username = models.CharField('Username', max_length=90)
    userpassword = models.CharField('Password', max_length=90)
    userdate = models.DateTimeField('date registered', null=True)
    userDob = models.DateTimeField('date of birth', null=True)
    useremail = models.EmailField('E-mail', null=True)

    avatar = models.ImageField(upload_to= 'images', null=True, blank=True)
    avatar_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

#cleaned up usermodel
class forum_user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_dob = models.DateTimeField('date of birth', null=True)
    avatar = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.user.username




class forumPost(models.Model):
    forumSubCategory = models.ForeignKey(forumSubCategory, on_delete = models.CASCADE)
    idUser = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length = 90)
    content_text = models.CharField(max_length = 500)
    date_stamp = models.DateTimeField('date published')
    is_edited = models.BooleanField(default=False)

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
    edited = models.BooleanField(default=False)

    def publish(self):
        self.date_stamp = timezone.now()
        self.save()

    def __str__(self):
        return self.content_text