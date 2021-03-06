from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from forums.models import forumCategory, forumPost, forumSubCategory,thread, user

from django.views.decorators.csrf import requires_csrf_token

from home.forms import UserNameForm, PostForm, Signupform, ReplyForm, SearchForm, Edit_form, PostCategoryForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from axes.decorators import watch_login
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

forumTitleList = forumCategory.objects.all()
forumSubCategoryList = forumSubCategory.objects.all()

searchForm = SearchForm()
contextDefault = {'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList, 'searchForm': searchForm}



def index(request):

    contextCategory = contextDefault.copy()

    return render(request,"home/index.html", contextCategory)

#list of forum topics along with the ones that can be edited
def post_list(request):
    posts  = forumPost.objects.all()
    if request.user.is_authenticated():
        context = contextDefault.copy()
        context.update({'posts': posts, 'username':request.user})
            #{'posts': posts, 'username':request.user, 'forumTitleList': forumTitleList, 'forumPostList':
        # forumSubCategoryList}
    else:
        context = contextDefault.copy()
        context.update({'posts':posts})
            #{'posts':posts, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}
    return render(request, "home/post_list.html", context)



#listing forumSubcats
def forum_posts(request, forum_id):
    forumPostList = forumPost.objects.filter(forumSubCategory__idForumCategory= forum_id)
    forumSubCategoryList = forumSubCategory.objects.filter(idForumCategory__id = forum_id)
    contextCategory = contextDefault.copy()
    title = forumCategory.objects.get(pk=forum_id).title
    contextCategory.update({'forumPostList': forumPostList, 'forumSubCategoryList': forumSubCategoryList,
                            'title':title})
        #{'forumTitleList': forumTitleList, 'forumPostList': forumPostList
         #              , 'forumSubCategoryList': forumSubCategoryList}
    return render(request,"home/forumposts.html", contextCategory)

#forum topics
def post_messages(request, post_id):

    forumPostMessages = forumPost.objects.filter(forumSubCategory__id = post_id)
    contextCategory = contextDefault.copy()
    title = forumSubCategory.objects.get(pk = post_id).title

    contextCategory.update({'forumPostMessages' : forumPostMessages, 'title':title})
        #'forumPostMessages' : forumPostMessages, 'forumTitleList': forumTitleList, 'forumPostList':
    # forumSubCategoryList}

    return render(request,"home/postpage.html", contextCategory)

#forum topic threads
def thread_view(request, post_id):

    threadList = thread.objects.filter(idForumPost__id = post_id)
    paginator = Paginator(threadList, 10)  # Show 5 threadposts per page
    page = request.GET.get('page')

    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)

    mainPost = forumPost.objects.get(pk=post_id)

    contextCategory = contextDefault.copy()

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
        form=ReplyForm()

    threadList = thread.objects.filter(idForumPost__id=post_id)
    paginator = Paginator(threadList, 10)  # Show 5 threadposts per page
    page = request.GET.get('page')

    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)


    contextCategory.update({'threadList' : threads,
                            'form':form,
                            'current_path' : get_current_path(request),
                            'mainPost' : mainPost,
                            })
    #{'threadList' : threadList, 'form':form, 'forumTitleList': forumTitleList, 'forumPostList': forumSubCategoryList}

    return render(request,"home/threadpage.html", contextCategory)

#a different sign in form
#@login_required
def home(request):
    context = contextDefault.copy()
    title = 'Please Log in'
    context.update({'title': title,})
    return render(request, 'registration/login.html', context)


#signing in an existing user

@watch_login
def signlog_in(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == "POST":
        form = UserNameForm(request.POST, )

        if form.is_valid():
            denizen = form.save(commit=False)

            if User.objects.get(username=denizen.username):
                user = authenticate(username=denizen.username, password=denizen.userpassword)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                    else:
                        return HttpResponse("Bad request")
                return redirect('index')

    else:
        form = UserNameForm()


    context = contextDefault.copy()
    title = 'Please Log in'
    context.update({'title':title, 'form': form})
    return render(request, 'home/post_edit.html', context)

#signing up new user view
def sign_up(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == "POST":

        form = Signupform(request.POST, request.FILES)

        if form.is_valid():
            denizen = form.save(commit=False)

            denizen.avatar = form.cleaned_data["avatar"]

            denizen.username = denizen.username.lower()

            denizen.save()

            #m.model_pic = form.cleaned_data['image']
            #m.save()


            user = User.objects.create_user(denizen.username, denizen.useremail, denizen.userpassword)
            user.save()
            denizen.user = user
            denizen.save()

            if User.objects.get(username=denizen.username):
                user = authenticate(username=denizen.username, password=denizen.userpassword)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                    else:
                        return HttpResponse("Bad request")
                return redirect('index')

    else:
        form = Signupform()

    context = contextDefault.copy()
    title = 'Please sign up using the form below'
    context.update({'title': title, 'form': form})
    return render(request, 'home/signup.html', context)

def post_new_cat(request):

    if not request.user.is_authenticated():
        return redirect('signlog_in')

    current_user = request.user
    if request.method == "POST":
        form = PostCategoryForm(request.POST)

    else:
        form = PostCategoryForm()

    if form.is_valid():
        post_cat = form.save(commit=False)
        return post_new(request, post_cat.pk)

    context = contextDefault.copy()
    title = 'Add new Post'
    context.update({'title': title, 'form': form})
    return render(request, 'home/post_cat_select.html', context)

#adding a new post view
def post_new(request, pk):

    if not request.user.is_authenticated():
        return redirect('signlog_in')


    current_user = request.user
    post_subcats = forumSubCategory.objects.filter(idForumCategory_id = pk)

    context = contextDefault.copy()
    title = 'Add new Post'
    context.update({'title': title, 'post_subcats':post_subcats})
    return render(request, 'home/post_edit.html', context)

def post_new_thread(request, pk):

    if not request.user.is_authenticated():
        return redirect('signlog_in')

    if request.method == "POST":
        form = PostForm(request.POST)

    else:
        form = PostForm()

    if form.is_valid():
        post = form.save(commit=False)
        post.idUser = User.objects.get(username=request.user.username)
        post.forumSubCategory = forumSubCategory.objects.get(pk=pk)
        post.publish()
        post.save()
        return redirect('index')
    context = contextDefault.copy()
    title = 'Add new Post'
    context.update({'title': title, 'form': form})
    return render(request, 'home/post_new.html', context)


#list of posts that can be edited
def post_edit(request, pk):

    post = get_object_or_404(forumPost, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_edited = True
            post.publish()
            return thread_view(request, pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'home/post_edit.html', {'form': form})

def profile_edit(request):

    profile = get_object_or_404(user, username = request.user.username)
    if request.method == "POST":
        form = Edit_form(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('profile_view')
    else:
        form = Edit_form(instance=profile)
    return render(request, 'home/profile_edit.html', {'form': form})

#search results
def post_search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searchItem = form.save(commit=False)
            searchResults = thread.objects.filter(content_text__contains=searchItem.content_text)
            context=contextDefault.copy()
            context.update({'posts': searchResults, 'username':request.user,})
                #{'posts': searchResults, 'username':request.user, 'forumTitleList': forumTitleList, 'forumPostList':
                #forumSubCategoryList}
            return render(request, "home/post_list.html", context)

        else:
            return redirect('index')

def log_out(request):
    logout(request)
    return redirect('index')


#getting current path
def get_current_path(request):
    return request.get_full_path()


#getting current path
def profile_view(request):
    if not request.user.is_authenticated():
        return redirect('signlog_in')

    context = contextDefault.copy()
    context.update({'username': request.user, 'avatar':request.user.user.avatar.url, 'email':request.user.user.useremail
    ,'dob':request.user.user.userDob,})
    return render(request, "home/profile.html", context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/password_edit.html', {
        'form': form
    })










