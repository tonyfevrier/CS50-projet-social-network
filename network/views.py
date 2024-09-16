from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import User, Post
import json


def index(request):
    return render(request, "network/index.html")


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
    

@login_required
def register_post(request):  
    # Register the post
    if request.method != "POST":
        return JsonResponse({'error':'The method of submission should be post'}, status=400)
         
    data = json.loads(request.body)  
    Post.objects.create(user=request.user, text=data.get('post_content'))
    return JsonResponse({'message':'post sent successfully'}, status=200)


def view_some_posts(request, whichposts):
    """Returns some posts depending on the button clicked in the navbar"""
    if whichposts == "all":
        return JsonResponse([post.serialize() for post in Post.objects.order_by('-date').all()], safe=False)
    else:
        if request.user.is_authenticated:
            # Recover the users the request user follows
            following = User.objects.get(username=request.user).following

            # Recover the posts corresponding to these users  
            return JsonResponse([post.serialize() for post in Post.objects.filter(user__username__in=following).order_by('-date').all()], safe=False)
        else:
            return JsonResponse({'message':'You must log in to access this page'}, status=404)


def view_profile(request, username):
    # Load user informations and all posts
    profile_user = User.objects.get(username = username)
    posts = Post.objects.filter(user = profile_user).order_by('-date')
    
    return JsonResponse({'user_stats':profile_user.serialize(),
                         'posts': [post.serialize() for post in posts],
                         'userisowner':request.user.username == username,
                         'userisfollower':request.user.username in profile_user.followers})


def follow_or_unfollow(request, username):
    # Look if request.user follows username
    profile_user = User.objects.get(username = username)
    request_user = User.objects.get(username = request.user.username)
    userisfollower = request.user.username in profile_user.followers

    if userisfollower:
        # Delete request user from followers of profile_user
        profile_user.followers.remove(request.user.username)

        # Delete profile_user from following of request.user
        request_user.following.remove(username)
    else:
        profile_user.followers.append(request.user.username)
        request_user.following.append(username)
    
    profile_user.save()
    request_user.save()
    return JsonResponse({'message':"Update correctly done"},status = 200)
    
