from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import Http404
from forums.models import forumCategory, forumPost, forumSubCategory,thread

from django.views.decorators.csrf import requires_csrf_token

from home.forms import UserNameForm
from django.http import HttpResponseRedirect

forumTitleList = forumCategory.objects.all()
forumSubCategoryList = forumSubCategory.objects.all()



def index(request):
    forumTitleList = forumCategory.objects.all()
    forumPostList = forumSubCategory.objects.all()[:5]

    contextCategory = {'forumTitleList': forumTitleList, 'forumPostList': forumPostList}

    return render(request,"home/index.html", contextCategory)

def post_list(request):
    posts  = forumPost.objects.all()
    context = {'posts':posts}
    return render(request, "home/post_list.html", context)




def forum_posts(request, forum_id):
    forumPostList = forumPost.objects.filter(forumSubCategory__id = forum_id)
    contextCategory = {'forumTitleList': forumTitleList, 'forumPostList': forumPostList
                       , 'forumSubCategoryList': forumSubCategoryList}

    return render(request,"home/forumposts.html", contextCategory)

def post_messages(request, post_id):
    forumPostMessages = thread.objects.filter(idForumPost__id = post_id)
    contextCategory = {'forumPostMessages' : forumPostMessages}

    return render(request,"home/postpage.html", contextCategory)



def get_username(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = UserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            username = request.emailaddress
            password =request.password


            context = {'username':username, 'password':password}
            return render(request,'home/signin.html', context)

    else:
        form = UserNameForm()  # An unbound form

    return render(request,'home/signin.html', {
        'form': form,
    })






