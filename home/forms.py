from django import forms
from forums.models import forumPost, user, thread

class UserNameForm(forms.ModelForm):

    class Meta:
        model = user
        fields = ('username', 'userpassword',)

class PostForm(forms.ModelForm):

    class Meta:
        model = forumPost
        fields = ('title', 'content_text',)

class Signupform(forms.ModelForm):

    class Meta:
        model = user
        fields = ('username', 'userpassword', 'useremail')

class ReplyForm(forms.ModelForm):

    class Meta:
        model = thread
        fields = ('content_text' ,)

class SearchForm(forms.ModelForm):

    class Meta:
        model = thread
        fields = ('content_text' ,)