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
    logged_in = request.user
    if request.method == "POST":
        post = request.POST["post"]
        new = UserPosts.objects.create(user=request.user, post=post)
        posts = UserPosts.objects.all()
        # user = request.user
    
    if user == "all":
        posts = UserPosts.objects.all()
    elif user == "user":
        posts = UserPosts.objects.filter(user=request.user)
    elif user != "user" and user != "all" and user != "post":
        user1 = User.objects.get(username=user)
        if user1 != logged_in:
            prof_user = user1
        posts = UserPosts.objects.filter(user=user1)
    
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, "network/index.html", {"not_logged_in_user":prof_user, "form":NewPostForm(), 'page_obj': page_obj})

