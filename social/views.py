from django.shortcuts import render
from django.views.generic.list import ListView
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



