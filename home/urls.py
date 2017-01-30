from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from axes.decorators import watch_login

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^(?P<forum_id>[0-9]+)/$', views.forum_posts, name='forum_posts'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_messages, name='post_messages'),
    url(r'^threads/(?P<post_id>[0-9]+)/$', views.thread_view, name='thread_view'),
    url(r'^login/$', views.signlog_in, name='signlog_in'),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^signin/$', views.sign_up, name='sign_up'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^searchpage/$', views.post_search, name='post_search'),
    url(r'^profile/$', views.profile_view, name='profile_view'),


]

urlpatterns += staticfiles_urlpatterns()