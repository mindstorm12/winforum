from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^(?P<forum_id>[0-9]+)/$', views.forum_posts, name='forum_posts'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_messages, name='post_messages'),
    url(r'^login/$', views.signlog_in, name='signlog_in'),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^signin/$', views.sign_up, name='sign_up'),
    url(r'^logout/$', views.log_out, name='log_out'),

]

urlpatterns += staticfiles_urlpatterns()