from django import forms
from django.forms import ModelForm, Textarea, PasswordInput
from forums.models import forumPost, user, thread
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField



class UserNameForm(forms.ModelForm):

    class Meta:
        model = user
        fields = ('username', 'userpassword',)
        widget = {
         'userpassword' : PasswordInput(),
        }

class PostForm(forms.ModelForm):

    class Meta:
        model = forumPost
        fields = ('forumSubCategory','title', 'content_text',)
        widgets = {
            'content_text': Textarea(attrs={'cols': 80, 'rows': 4}),
        }
        labels = {
            'content_text': _('Post'),
            'forumSubCategory': _('Sub-Category'),
        }


class Signupform(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = user
        fields = ('username', 'userpassword', 'useremail')


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