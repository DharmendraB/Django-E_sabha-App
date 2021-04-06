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
]
