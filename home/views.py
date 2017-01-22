from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from forums.models import forumCategory, forumPost, forumSubCategory,thread, user

from django.views.decorators.csrf import requires_csrf_token

from home.forms import UserNameForm, PostForm, Signupform, ReplyForm, SearchForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

forumTitleList = forumCategory.objects.all()
forumSubCategoryList = forumSubCategory.objects.all()
searchForm = SearchForm()



def index(request):
    contextCategory = {'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList, 'searchForm': searchForm}

    return render(request,"home/index.html", contextCategory)

#list of forum topics along with the ones that can be edited
def post_list(request):
    posts  = forumPost.objects.all()
    if request.user.is_authenticated():
        context = {'posts': posts, 'username':request.user, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}
    else:
        context = {'posts':posts, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}
    return render(request, "home/post_list.html", context)



#listing forumSubcats
def forum_posts(request, forum_id):
    forumPostList = forumPost.objects.filter(forumSubCategory__idForumCategory= forum_id)
    forumSubCategoryList = forumSubCategory.objects.filter(idForumCategory__id = forum_id)
    contextCategory = {'forumTitleList': forumTitleList, 'forumPostList': forumPostList
                       , 'forumSubCategoryList': forumSubCategoryList}

    return render(request,"home/forumposts.html", contextCategory)

#forum topics
def post_messages(request, post_id):

    forumPostMessages = forumPost.objects.filter(forumSubCategory__id = post_id)
    contextCategory = {'forumPostMessages' : forumPostMessages, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}

    return render(request,"home/postpage.html", contextCategory)

#forum topics
def thread_view(request, post_id):

    threadList = thread.objects.filter(idForumPost__id = post_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
    else:
        form = ReplyForm()

    if form.is_valid():
        threadreply = form.save(commit=False)
        threadreply.idForumPost=forumPost(pk=post_id)
        threadreply.idUser = request.user
        threadreply.publish()
        threadreply.save()

    contextCategory = {'threadList' : threadList, 'form':form, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}

    return render(request,"home/threadpage.html", contextCategory)


def get_username(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = UserNameForm(request.POST)
        if form.is_valid():
            username = request.emailaddress
            password =request.password


            context = {'username':username, 'password':password, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}
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

#signing up new user view
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

#adding a new post view
def post_new(request):
    current_user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)

    else:
        form = PostForm()

    if form.is_valid():
        post = form.save(commit=False)
        post.idUser = User.objects.get(username=current_user.username)

        post.forumSubCategory = forumSubCategory.objects.get (pk=1)
        post.publish()
        post.save()
        return redirect('post_list')

    return render(request, 'home/post_edit.html', {'form': form})

#list of posts that can be edited
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

#search results
def post_search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searchItem = form.save(commit=False)
            searchResults = thread.objects.filter(content_text__contains=searchItem.content_text)
            context = {'posts': searchResults, 'username':request.user, 'forumTitleList': forumTitleList, 'forumPostList':
                forumSubCategoryList}
            return render(request, "home/post_list.html", context)

        else:
            return redirect('index')

def log_out(request):
    logout(request)
    return redirect('post_list')





