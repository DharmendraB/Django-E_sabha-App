from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from social.models import MyProfile, MyPost, PostCommet, PostLike, FollowUser,Question

# Register your models here.
class FollowUserAdmin(ModelAdmin):
    list_display = ["profile","followed_by"]
    search_fields = ["profile","followed_by"]
    list_filter = ["profile","followed_by"]    
admin.site.register(FollowUser, FollowUserAdmin)

class MyPostAdmin(ModelAdmin):
    list_display = ["subject","pub_date","uploaded_by"]
    search_fields = ["subject","msg"]
    list_filter = ["uploaded_by","pub_date"]    
admin.site.register(MyPost, MyPostAdmin)

class MyProfileAdmin(ModelAdmin):
    list_display = ["name","gender"]
    search_fields = ["name","status"]
    list_filter = ["status"]    
admin.site.register(MyProfile, MyProfileAdmin)

class PostCommetAdmin(ModelAdmin):
    list_display = ["post","msg","pub_date"]
    search_fields = ["post","msg","commited_by"]
    list_filter = ["pub_date","flag"]    
admin.site.register(PostCommet, PostCommetAdmin)

class PostLikeAdmin(ModelAdmin):
    list_display = ["post","liked_by"]
    search_fields = ["post","liked_by"]
    list_filter = ["pub_date"]    
admin.site.register(PostLike, PostLikeAdmin)

class QuestionAdmin(ModelAdmin):
    list_display = ["user","subject"]
    search_fields = ["user","subject"]
    list_filter = ["pub_date"]    
admin.site.register(Question, QuestionAdmin)