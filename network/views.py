import json
from errno import ESTALE
from unittest import removeResult
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from flask_login import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from sqlalchemy import true

from .models import Follow, Like, Post, User


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

def profile(request):
    content_follower = Follow.objects.filter(creator = request.user.username)
    content_following = Follow.objects.filter(follower = request.user.username)
    follower = 0
    following = 0
    for info in content_following:
        following += 1
    for info in content_follower:
        follower += 1
    information = {
    'follower': follower,
    'following': following
    }
    return render(request, "network/profile.html", information)

@csrf_exempt
def posts(request, post):
    # Filter emails returned based on mailbox
    if post == "current":
        username = request.user.username
        posts = Post.objects.filter(creator = username)
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post_content.serialize() for post_content in posts], safe=False)
    elif post == "all":
        data = json.loads(request.body)
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10)
        page_number = data.get("page")
        page_obj = paginator.get_page(page_number)
        return JsonResponse([post_content.serialize() for post_content in page_obj], safe=False)
    elif post == "following":
        username = request.user.username
        if(username):
            posts = []
            following = Follow.objects.filter(follower = username)
            count = 0
            post_count = 0
            for x in following:
                post = Post.objects.filter(creator = following[count].creator)
                for post_content in post:
                    json_post = post[post_count].serialize()
                    post_count += 1
                    posts.append(json_post)
                post_count = 0
                count += 1
            return JsonResponse(posts, safe=False)
        else:
            return render(request, "network/index.html")

@csrf_exempt
def likes(request, id):
    username = request.user.username
    if(username):
        if request.method == "PUT":
            data = json.loads(request.body)
            if(data["liked"] == "True"):
                Like.objects.create(
                    liker = request.user.username, 
                    post_id = id
                )
            else:
                Like.objects.filter(
                    liker = request.user.username,
                    post_id = id
                ).delete()
            return JsonResponse({"liked": "1"})
        else:
            value = Like.objects.filter(post_id = id, liker = username)
            if value.exists():
                return JsonResponse({"liked": "1"})
            else:
                return JsonResponse({"liked": "0"})
   

def alllikes(request, id):
    values = Like.objects.filter(post_id = id)
    likes = 0
    for value in values:
        likes += 1
    return JsonResponse({"likes": likes})

def following(request):
    return render(request, "network/following.html")


def getuser(request, id):
    content_follower = Follow.objects.filter(creator = id)
    content_following = Follow.objects.filter(follower = id)
    follower = 0
    following = 0
    for info in content_following:
        following += 1
    for info in content_follower:
        follower += 1
    follows = 0
    information = {
    'username': id,
    'follower': follower,
    'following': following,
    'follows': follows
    }
    if id == request.user.username:
        return render(request, "network/profile.html", information)
    return render(request, "network/profiles.html", information)

@csrf_exempt
def getuserposts(request, id):
    data = json.loads(request.body)
    posts = Post.objects.filter(creator = id)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = data.get("page")
    page_obj = paginator.get_page(page_number)
    return JsonResponse([post_content.serialize() for post_content in page_obj], safe=False)


@csrf_exempt
def newpost(request):
    username = request.user.username
    if(username):
        data = json.loads(request.body)
        content = data["content"]
        if request.method == "POST":
            Post.objects.create(
                creator = username,
                content = content 
            )
    return JsonResponse({"Posted": "1"})

@csrf_exempt
def follow(request):
    username = request.user.username
    if(username):
        if request.method == "POST":
            data = json.loads(request.body)
            content = data["content"]
            value = Follow.objects.filter(follower = username, creator = content)
            if value.exists():
                return JsonResponse({"follows": "1"})
            else:
                return JsonResponse({"follows": "0"})
        if request.method == "PUT":
            data = json.loads(request.body)
            content = data["follows"]
            if content == "true":
                Follow.objects.create(follower = username, creator = data["creator"])
            else:
                Follow.objects.filter(follower = username, creator = data["creator"]).delete()
            return JsonResponse({"follows": "1"})
    return JsonResponse({})