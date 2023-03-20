from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from itertools import chain
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import *

@login_required(login_url='login')
def index(request):
    
    currentuser = User.objects.get(id=request.user.id)

    # Get all posts and sort by time desc
    posts = Post.objects.all().order_by("-time")

    # Paginate the pages
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    #Check which posts the currentuser has liked
    posts_liked = currentuser.posts_liked.all()

    return render(request, "network/index.html", {
        "allposts":posts, "page_posts":page_posts,
        "posts_liked": posts_liked,
    })


def newpost(request):
    content = request.POST.get("content")
    currentuser = User.objects.get(id=request.user.id)

    # Create new post, save it, and redirect to allposts page
    post = Post(content=content, user=currentuser)
    post.save()
    return HttpResponseRedirect(reverse("index"))


def profile(request, userid):
    currentuser = User.objects.get(id=request.user.id)
    user = User.objects.get(id=userid)

    # Get follower numbers
    followersnum = user.followers.count()
    followingnum = user.user_following.all().count()

    # Check if currentuser follows user
    followers = user.followers.all()
    if currentuser in followers:
        btnid = "unfollowbtn"
        btnhtml = "Unfollow"
    else:
        btnid = "followbtn"
        btnhtml = "Follow"

    # Get all the user's posts
    userposts = user.user_posts.all().order_by("-time")

    # Paginate the pages
    paginator = Paginator(userposts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "user":user, "followersnum":followersnum,
        "followingnum":followingnum, "userposts":userposts,
        "currentuser":currentuser, "btnid": btnid, "btnhtml": btnhtml,
        "page_posts":page_posts,
        
    })

def follow(request, userid):
    currentuser = User.objects.get(id=request.user.id)
    user = User.objects.get(id=userid)

    # Adding the loggedin user as a follower to the profile/user
    user.followers.add(currentuser)
    return HttpResponse()

def unfollow(request, userid):
    currentuser = User.objects.get(id=request.user.id)
    user = User.objects.get(id=userid)

    # Removing the loggedin user as a follower to the profile/user
    user.followers.remove(currentuser)
    return HttpResponse()

def following(request):
    currentuser = User.objects.get(id=request.user.id)
    followed_users = currentuser.user_following.all()
    num_followed_users = currentuser.user_following.all().count()

    # Get all the posts by the users the curretuser follows (1st way)
    qlist = []
    for i in range(num_followed_users):
        q = followed_users[i].user_posts.all()
        qlist.append(q)

    # Chain them into 1 list of objects(posts) and then sort them by time
    posts = list(chain(*qlist))
    sorted_posts = sorted(posts, key=lambda x: x.time, reverse=True)

    # BOB's way to find followed posts (2nd way)
    # filtered_posts = Post.objects.filter(user__in=followed_users).order_by("-time")

    # Paginate the pages
    paginator = Paginator(sorted_posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    #Check which posts the currentuser has liked
    posts_liked = currentuser.posts_liked.all()

    return render(request, "network/following.html",{
        "sorted_posts":sorted_posts, "currentuser":currentuser,
        "page_posts":page_posts, "posts_liked": posts_liked,

    })

@csrf_exempt
def edit(request, postid):
    currentuser = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=postid)

    # Verify that the editor is the owner of the post
    if currentuser.id != post.user.id:
        return JsonResponse({
            "message": "Unable to edit post belonging to another user."
        }, status=400)
    
    # Get Json data from JS
    data = json.loads(request.body)

    # Get new edited content
    content = data.get("content", "")

    # Edit Post
    post.content = content
    post.save()

    return JsonResponse({
        "message": "Post edited successfully."
        }, status=201)


@csrf_exempt
def like(request):
    # Get Json data from JS
    data = json.loads(request.body)

    # Get id of the liked post
    postid = data.get("postid", "")

    currentuser = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=postid)

    # Like the post
    post.users_liked.add(currentuser)

    # Number of new likes
    likecount = post.users_liked.count()

    return JsonResponse({
        "likecount": likecount,
        })


@csrf_exempt
def unlike(request):
    # Get Json data from JS
    data = json.loads(request.body)

    # Get id of the liked post
    postid = data.get("postid", "")

    currentuser = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=postid)

    # Like the post
    post.users_liked.remove(currentuser)

    # Number of new likes
    likecount = post.users_liked.count()

    return JsonResponse({
        "likecount": likecount,
        })


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
