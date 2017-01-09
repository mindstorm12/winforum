from django import forms
from forums.models import forumPost

class UserNameForm(forms.Form):
    username = forms.CharField(label='Username', max_length = 100)
    password = forms.CharField(label='Password', max_length = 100)

class PostForm(forms.ModelForm):

    class Meta:
        model = forumPost
        fields = ('title', 'content_text',)
