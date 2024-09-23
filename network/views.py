from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator

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
        posts = Post.objects.order_by('-date').all() 
    else:
        if request.user.is_authenticated:
            # Recover the users the request user follows
            following = User.objects.get(username=request.user).following

            # Recover the posts corresponding to these users 
            posts = Post.objects.filter(user__username__in=following).order_by('-date').all() 
        else:
            return JsonResponse({'message':'You must log in to access this page'}, status=404)
    
    # Create a paginator with ten posts pages, get the actual page and send the post informations
    p = Paginator(posts, 10)
    actual_page = p.page(request.GET.get("param1"))
    return JsonResponse({"posts":[post.serialize() for post in actual_page.object_list],
                         "previous":actual_page.has_previous(),
                         "next":actual_page.has_next(),
                         "number_posts":len(posts),
                         "requestuser":request.user.username}, safe=False)


def view_profile(request, username):
    # Load user informations and all posts
    profile_user = User.objects.get(username = username)
    posts = Post.objects.filter(user = profile_user).order_by('-date')
    
    return JsonResponse({'user_stats':profile_user.serialize(),
                         'posts': [post.serialize() for post in posts],
                         'userisowner':request.user.username == username,
                         'userisfollower':request.user.username in profile_user.followers,
                         'requestuser':request.user.username})


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


@login_required
def edit_post(request, id):
    if request.method != "POST":
        return JsonResponse({'error':'Post edition failed'}, status=404) 
 
    # Get the text of the textarea and register it in the database
    data = json.loads(request.body)
    post = Post.objects.get(id=id)
    post.text = data.get('content')
    post.save()

    return JsonResponse({'message':'Post edited'}, status=200) 


def like_post(request, id):
    # Get the good post and modify the list of likers
    post = Post.objects.get(id=id)

    if (request.user.username) in  post.likes:
        post.likes.remove(request.user.username)
    else:
        post.likes.add(request.user.username)
    post.save()

    return JsonResponse({'post':post.serialize()}, status=200) 
