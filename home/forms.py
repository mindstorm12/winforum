from django import forms
from django.forms import ModelForm, Textarea, PasswordInput
from forums.models import forumPost, user, thread, forumSubCategory, forumCategory
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User
from django.db import models



class UserNameForm(forms.ModelForm):

    class Meta:
        model = user
        fields = ('username','userpassword')

class PostCategoryForm(forms.ModelForm):

    class Meta:
        model = forumCategory
        fields = ('title',)


class PostForm(forms.ModelForm):

    class Meta:
        model = forumPost
        fields = ('title', 'content_text',)
        widgets = {
            'content_text': Textarea(attrs={'cols': 80, 'rows': 4}),
        }
        labels = {
            'content_text': _('Post'),
            'forumSubCategory': _('Sub-Category'),
        }


class Signupform(forms.ModelForm):
    captcha = CaptchaField()


    #experimenting image
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 4096
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

    #end of image upload

    #avatar = forms.ImageField()
    #avatar = clean_avatar()
    class Meta:
        model = user
        fields = ('username','userpassword','avatar',)
        widgets = {
            'userpassword': forms.PasswordInput(),
        }



class ReplyForm(forms.ModelForm):

    class Meta:
        model = thread
        fields = ('content_text' ,)
        labels = {
            'content_text': _('Reply'),
        }
        widgets = {
            'content_text': Textarea(attrs={'cols': 80, 'rows': 4}),
        }

class SearchForm(forms.ModelForm):

    class Meta:
        model = thread
        fields = ('content_text' ,)
        labels = {
            'content_text': _(''),
        }


class Edit_form(forms.ModelForm):

    captcha = CaptchaField()

    #experimenting image
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 4096
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

    #end of image upload

    #avatar = forms.ImageField()
    #avatar = clean_avatar()
    class Meta:
        model = user
        fields = ('avatar',)