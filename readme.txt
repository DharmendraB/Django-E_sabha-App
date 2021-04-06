#all in one project (not included Virtual Env)

//Terminal Commands
#Startproject
$ django-admin startproject E_sabha 

# go to manage.py inside project
$ cd E_s

#Create Apps
$ django-admin startapp social

#Run Django Application
$ python manage.py runserver

#Bootstrap install in django
>>pip install django-crispy-forms

#Create Table and database 
$ python manage.py makemigrations
$ python manage.py migrate

.........................................settings.py......................................
// Settings.py Add Code
INSTALLED_APPS = [
    'social.apps.SocialConfig',
    'registration',
    ...
    'crispy_forms',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#Set TIME_ZONE
TIME_ZONE = 'Asia/Kolkata'

#Managing Media Code here
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

#Registration form import Code here
ACCOUNT_ACTIVATION_DAYS=3
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_HOST_USER= 'xxx@gmail.com'
EMAIL_HOST_PASSWORD= xxxxx
EMAIL_PORT= 587
EMAIL_USE_TLS= True

#Direct Login Redirect Code here
LOGIN_REDIRECT_URL = "/"
..........................Settings.py End.................................................

............................................Main urls.py..................................
#Main urls.py Code
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social.urls')),
    path('', RedirectView.as_view(url="social/")),
    path('accounts/', include('registration.backends.default.urls')),     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
..............Main urls.py End.......................................................

......................................urls.py........................................
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from social import views
urlpatterns = [
     path('home/', views.HomeView.as_view()),
     path('about/', views.AboutView.as_view()),
     path('contact/', views.ContactView.as_view()),
     path('', RedirectView.as_view(url="home/")),
    path('question/create/', views.QuestionCreate.as_view(success_url="/social/home")),
#Post Related URLS    
    path('mypost/create/', views.MyPostCreate.as_view(success_url="/social/mypost")),
    path('mypost/edit/<int:pk>/', views.MyPostUpdateView.as_view(success_url="/social/mypost")),
    path('mypost/delete/<int:pk>', views.MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/', views.MyPostListView.as_view()),
    path('mypost/<int:pk>', views.MyPostDetailView.as_view()),
    path('mypost/like/<int:pk>', views.like),
    path('mypost/unlike/<int:pk>', views.unlike),
#Profile Related URLS
    path('profile/', views.MyProfileListView.as_view()),
    path('profile/<int:pk>', views.MyProfileDetailView.as_view()),
    path('profile/follow/<int:pk>', views.follow),
    path('profile/unfollow/<int:pk>', views.unfollow),
    path('profile/edit/<int:pk>/', views.ProfileUpdateView.as_view(success_url="/social/")),
]......................................end urls.py................................................

...............................................views.py......................................
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView,DeleteView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from social.models import MyProfile,MyPost,PostCommet,PostLike,FollowUser,Question
from django.http.response import HttpResponseRedirect
from django.db.models import Q
# Create your views here.
#Home Disply Followed post list code
@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "social/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        FollowedList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        FollowedList2 = []
        for e in FollowedList:
            FollowedList2.append(e.profile)            
        search = self.request.GET.get('uq')
        if search == None:
            search =""
        PostList = MyPost.objects.filter(Q(uploaded_by__in=FollowedList2)).filter(Q(subject__icontains = search) | Q(msg__icontains = search)).order_by("-id")        
        for p1 in PostList:
            p1.liked = False
            ob = PostLike.objects.filter(post = p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            postlikecount = PostLike.objects.filter(post = p1)
            p1.likecount = postlikecount.count()           
        context["mypost_list"] = PostList
        return context
    
# AboutUs Display Code 
class AboutView(TemplateView):
    template_name = "social/about.html"
# ContactUs Display Code 
class ContactView(TemplateView):
    template_name = "social/contact.html"

# Profile update Code 
@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    model = MyProfile  
    fields = ["name","age","gender","status","phone","address","description","image"]
    # Use this for all Field disply user
    # fields = "__all__" 

# Question Create Code 
@method_decorator(login_required, name="dispatch")
class QuestionCreate(CreateView):
    model = Question
    fields = ["subject","msg"]
    def form_valid(self, form):
        self.object = form.save()  
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# Post Create Code 
@method_decorator(login_required, name="dispatch")
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject","msg","image"]
    def form_valid(self, form):
        self.object = form.save()  
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# AllPost Disply Code 
@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        search = self.request.GET.get('uq')
        if search == None:
            search =""

        # return Notice.objects.filter(branch=self.request.user.profile.branch).order_by("-id")[:10]
        return MyPost.objects.filter(Q(uploaded_by=self.request.user.myprofile)).filter(Q(subject__icontains = search) | Q(msg__icontains = search)).order_by("-id")

# Post Details Disply Code 
@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost

# Post Delete Code 
@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost

#Profile Display Code 
@method_decorator(login_required, name="dispatch")
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        search = self.request.GET.get('uq')
        if search == None:
            search =""

        # return Notice.objects.filter(branch=self.request.user.profile.branch).order_by("-id")[:10]
        ProfileList = MyProfile.objects.filter(Q(name__icontains = search) | Q(address__icontains = search) | Q(gender__icontains = search) | Q(status__icontains = search)).order_by("-id")
        for p1 in ProfileList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1, followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return ProfileList

# Post Details Display Code 
@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile

# Profile update Code 
@method_decorator(login_required, name="dispatch")
class MyPostUpdateView(UpdateView):
    model = MyPost 
    fields = ["subject","msg","image"]
    # Use this for all Field disply user
    # fields = "__all__" 

#Follow Link code    
def follow(request, pk):    
    UserData = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=UserData, followed_by=request.user.myprofile)
    return HttpResponseRedirect("/social/profile")

#UnFollow Link code 
def unfollow(request, pk):    
    UserData = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=UserData, followed_by=request.user.myprofile).delete()
    return HttpResponseRedirect("/social/profile")

#Like Link code 
def like(request, pk):    
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by=request.user.myprofile)
    return HttpResponseRedirect("/social/home")

#Un1like Link code 
def unlike(request, pk):    
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by=request.user.myprofile).delete()
    return HttpResponseRedirect("/social/home")
........................end views.py..............................................................................

.....................................................models.py....................................................
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
  
class MyProfile(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    gender = models.CharField(max_length=10, default="Male", choices=(("Male","Male"),("Female","Female")))  
    status = models.CharField(max_length=10, default="single", choices=(("single","single"),("married","married"),("widow","widow"),("seprated","seprated"),("commited","commited")))
    phone = models.CharField(validators=[RegexValidator("0?^[5-9]{1}\d{9}$")],max_length=20, null=True, blank=True)    
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)   
    # pip install pillow==6.0.0 --user
    image = models.ImageField(upload_to="social/images", default="") 
    def __str__(self):
        return "%s" % self.name
class MyPost(models.Model):
    image = models.ImageField(upload_to="social/images", default="") 
    subject = models.CharField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)    
    uploaded_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, blank=True, null=True)
    def __str__(self):
        return "%s" % self.subject

class PostCommet(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    msg = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)   
    commited_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE) 
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(("Racist","Racist"),("Abbusing","Abbusing")))  
    def __str__(self):
        return "%s" % self.msg

class PostLike(models.Model):    
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)    
    pub_date = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return "%s" % self.liked_by

class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE,related_name="Profile")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")    
    pub_date = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return "%s" % self.followed_by

class Question(models.Model):
    subject = models.CharField(max_length=500)
    msg = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=CASCADE, blank=True, null=True,unique=True)
    def __str__(self):
        return self.subject
.....................end models.py...........................................................

.......................................admin.py.............................................
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
......................end admin.py.......................................................

..................................................apps.py...............................
from django.apps import AppConfig
class SocialConfig(AppConfig):
    name = 'social'
    def ready(self):
        import social.mysignal
..................................................mysignal.py.............................
#this file used for user Profile create first time 
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from social.models import MyProfile
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kw):
    if created:
        MyProfile.objects.create(user=instance,name=instance.username)

............................................../social/_init_.py....................................
default_app_config = 'social.apps.SocialConfig'


.....................................Create Folder.........................................
E_sabha/media/social/images
E_sabha/static
#inside Social app
templates/social
templates/registration

.....................................html files.....................................................
E_sabha\social\templates\base.html
#social Folder
E_sabha\social\templates\social\about.html
E_sabha\social\templates\social\contact.html
E_sabha\social\templates\social\home.html
E_sabha\social\templates\social\myprofile_list.html
E_sabha\social\templates\social\myprofile_form.html
E_sabha\social\templates\social\myprofile_detail.html
E_sabha\social\templates\social\mypost_list.html
E_sabha\social\templates\social\mypost_form.html
E_sabha\social\templates\social\mypost_detail.html
E_sabha\social\templates\social\mypost_confirm_delete.html
E_sabha\social\templates\social\question_form.html
#registration
E_sabha\social\templates\registration\login.html
E_sabha\social\templates\registration\registration_form.html
