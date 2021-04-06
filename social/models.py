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