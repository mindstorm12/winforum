from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from forums.models import forumCategory, forumPost, forumSubCategory,thread, user

from django.views.decorators.csrf import requires_csrf_token

from home.forms import UserNameForm, PostForm, Signupform
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.contrib.auth import login, logout

forumTitleList = forumCategory.objects.all()
forumSubCategoryList = forumSubCategory.objects.all()



def index(request):
    forumTitleList = forumCategory.objects.all()
    forumPostList = forumSubCategory.objects.all()[:5]

    contextCategory = {'forumTitleList': forumTitleList, 'forumPostList': forumPostList}

    return render(request,"home/index.html", contextCategory)

def post_list(request):
    posts  = forumPost.objects.all()
    if request.user.is_authenticated():
        context = {'posts': posts, 'username':request.user}
    else:
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



def signlog_in(request):
    if request.method == "POST":
        form = UserNameForm(request.POST)
    else:
        form = UserNameForm()

    if form.is_valid():
        denizen = form.save(commit=False)

        if User.objects.get(username=denizen.username):
                user = authenticate(username=denizen.username, password=denizen.userpassword)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                    else:
                        return HttpResponse("Bad request")
                return redirect('post_list')
    return render(request, 'home/post_edit.html', {'form': form})

def sign_up(request):
    if request.method == "POST":
        form = Signupform(request.POST)
    else:
        form = Signupform()

    if form.is_valid():
        denizen = form.save(commit=False)

        user = User.objects.create_user(denizen.username, denizen.useremail, denizen.userpassword)
        user.save()

        if User.objects.get(username=denizen.username):
            user = authenticate(username=denizen.username, password=denizen.userpassword)
            if user is not None:
                if user.is_active:
                    login(request, user)

                else:
                    return HttpResponse("Bad request")
            return redirect('post_list')
    return render(request, 'home/post_edit.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
    else:
        form = PostForm()

    if form.is_valid():
        post = form.save(commit=False)
        post.idUser = user.objects.get(pk=1)
        post.forumSubCategory = forumSubCategory.objects.get (pk=1)
        post.publish()
        post.save()
        return redirect('post_list')

    return render(request, 'home/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(forumPost, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'home/post_edit.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('post_list')





