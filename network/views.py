import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewPostForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserPosts, Following
from django.core.paginator import Paginator


def index(request):

    posts = UserPosts.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"form":NewPostForm(), 'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def all_posts(request, user):
    prof_user=False
    show_foll = False
    logged_in = request.user
    #Adds new post to the UserPosts model
    #New post form is on the all_posts page, updates as soon as post made.
    if request.method == "POST":
        post = request.POST["post"]
        new = UserPosts.objects.create(user=request.user, post=post)
        new.save()
        posts = UserPosts.objects.all()
        
        
    #Selects all userposts
    posts = UserPosts.objects.all()
    print("posst", posts)
    #Selects all posts from the logged in user
    if user == "user":
        posts = UserPosts.objects.filter(user=request.user)
        show_foll = True
    elif user == "following":
        #UNION OPERATOR!!!!!!!!!!!!!
        followed = Following.objects.filter(user_id=request.user)
        posts = [i.following.username for i in followed]
        
    #Selects all the posts from the username on the link clicked
    elif user != "all" and user != "user" and user != "post":
        user1 = User.objects.get(username=user)
        #Changes Prof_user from false to a username,
        #this makes the html template add a follow button to
        #non-logged in user profiles.
        if user1 != logged_in:
            prof_user = user1
        show_foll = True
        posts = UserPosts.objects.filter(user=user1)
        
    #Sorts the post by time order
    posts = posts.order_by("-timestamp").all()

    #Paginates posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {"show_foll":show_foll, "not_logged_in_user":prof_user, "form":NewPostForm(), 'page_obj': page_obj})

@csrf_exempt
def follow_or_unfollow(request, user):
    if request.method == "PUT":
        followee = User.objects.get(username=user)
        try:
            new_follower = Following.objects.get(following=followee, user=request.user)
            #Insert the follower and followee into the following model, if not already followed.
            new_follower.delete()
            
            #Update the followee's followers.
            new_follow = User.objects.get(username=followee)
            new_follow.followers = new_follow.followers - 1
            new_follow.save()

            #Update the followers followed.
            new_followed = User.objects.get(username=request.user)
            new_followed.followed = new_followed.followed - 1
            new_followed.save()
        except:
            #Insert the follower and followee into the following model, if not already followed.
            new_follower = Following.objects.create(user=request.user, following=followee)
            new_follower.save()
            
            #Update the followee's followers.
            new_follow = User.objects.get(username=followee)
            new_follow.followers = new_follow.followers + 1
            new_follow.save()

            #Update the followers followed.
            new_followed = User.objects.get(username=request.user)
            new_followed.followed = new_followed.followed + 1
            new_followed.save()
    return HttpResponse(status=204)

def is_followed(request):
    followed = Following.objects.filter(user_id=request.user)
    foll = [i.following.username for i in followed]
    return JsonResponse(foll, safe=False)
