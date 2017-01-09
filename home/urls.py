from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^$',views.index, name = 'index'),
    url(r'^(?P<forum_id>[0-9]+)/$', views.forum_posts, name='forum_posts'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_messages, name='post_messages'),
    url(r'^login/$', views.get_username, name='get_username'),

]

urlpatterns += staticfiles_urlpatterns()