from django.contrib import admin

from .models import forumPost, user, thread, forumCategory, forumSubCategory

admin.site.register(forumPost)
admin.site.register(user)
admin.site.register(thread)
admin.site.register(forumCategory)
admin.site.register(forumSubCategory)