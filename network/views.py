from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt



from .models import User, Post, Follow, Like, Comment


def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    p = Paginator(posts, 10)
    number_of_pages = p.page_range
    current_page = request.GET.get('page')
    page_posts = p.get_page(current_page)
    current_user = request.user
    likes = Like.objects.all()
    liked_posts = []
    for like in likes:
        if like.user.id == current_user.id:
            liked_posts.append(like.post.id)
    comments = Comment.objects.all().order_by("id").reverse()
    return render(request, "network/index.html", {
        "posts" : page_posts,
        "number_of_pages" : number_of_pages,
        "current_page" : current_page,
        "liked_posts" : liked_posts, 
        "comments": comments,
    })
    
    
def post(request):
    if request.method == "POST":
        post_content = request.POST["post-content"]
        user = User.objects.get(pk=request.user.id)
        new_post = Post(user = user, content = post_content)
        new_post.save()
        return HttpResponseRedirect(reverse(index))
    
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("id").reverse()
    # Show only 10 posts per page
    p = Paginator(posts, 10)
    number_of_pages = p.page_range
    current_page = request.GET.get('page')
    page_posts = p.get_page(current_page)
    current_user = request.user
    likes = Like.objects.all()
    liked_posts = []
    for like in likes:
        if like.user.id == current_user.id:
            liked_posts.append(like.post.id)
    
    
    # Show number of followers and accounts that the user is following
    following = Follow.objects.filter(following = user)
    followers = Follow.objects.filter(followed = user)
    
    # Check if current user already follows the visited profile
    try:
        visitor = User.objects.get(pk=request.user.id)
    except:
        return render(request, "network/profile.html", {
        "posts" : page_posts,
        "number_of_pages" : number_of_pages,
        "current_page" : current_page,
        "user_name" : user.username,
        "following" : following,    
        "followers" : followers,
        "visited_user" : user,  
        "liked_posts" : liked_posts, 
    })
    
    followage = followers.filter(following_id=visitor)
    if not followage:
        followage == False
    else:
        followage == True
    return render(request, "network/profile.html", {
        "posts" : page_posts,
        "number_of_pages" : number_of_pages,
        "current_page" : current_page,
        "user_name" : user.username,
        "following" : following,    
        "followers" : followers, 
        "followage" : followage,
        "visitor" : visitor, 
        "visited_user" : user,  
        "liked_posts" : liked_posts, 
    })
    
    
def follow(request):
    followed = request.POST['followed']
    current_user_data = User.objects.get(pk=request.user.id)
    followed_user_data = User.objects.get(username=followed)
    f = Follow(following = current_user_data, followed = followed_user_data)
    f.save()
    user_id = followed_user_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


def unfollow(request):
    followed = request.POST['followed']
    current_user_data = User.objects.get(pk=request.user.id)
    followed_user_data = User.objects.get(username=followed)
    f = Follow.objects.get(following = current_user_data, followed = followed_user_data)
    f.delete()
    user_id = followed_user_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


def following(request, username):
    current_user = User.objects.get(pk=request.user.id)
    user_followings = Follow.objects.filter(following=current_user)
    posts = Post.objects.all().order_by("id").reverse()
    following_posts = []
    for post in posts:
        for followed_user in user_followings:
            if followed_user.followed == post.user:
                following_posts.append(post)
                
    p = Paginator(following_posts, 10)
    number_of_pages = p.page_range
    current_page = request.GET.get('page')
    page_posts = p.get_page(current_page)
    comments = Comment.objects.all().order_by("id").reverse()
    likes = Like.objects.all()
    liked_posts = []
    for like in likes:
        if like.user.id == current_user.id:
            liked_posts.append(like.post.id)
    
    return render(request, "network/following.html", {
        "posts" : page_posts,
        "number_of_pages" : number_of_pages,
        "current_page" : current_page,
        "comments": comments,
        "liked_posts" : liked_posts, 
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

@csrf_exempt
def edit(request, post_id):
    if request.method == "POST":
        edited_text = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.content = edited_text["content"]
        post.save()
         
    return JsonResponse({"alert": "Edited.", "edited_text": edited_text["content"]})

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    like.save()
    post.likes = post.likes + 1
    post.save()
    return JsonResponse({"alert": "Liked."})


def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    post.likes = post.likes - 1
    post.save()  
    return JsonResponse({"alert": "Unliked."})


@csrf_exempt
def delete_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id = post_id)
        post.delete()
        return JsonResponse({"alert": "Post Removed."})

def comment(request, post_id):
    if request.method == "POST":
        user= request.user
        post = Post.objects.get(pk=post_id)
        comment = request.POST['comment']
        
        newComment = Comment(
            writer = user,
            post = post,
            comment = comment,
        )   
        newComment.save()
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def delete_comment(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.filter(id = comment_id)
        comment.delete()
        return JsonResponse({"alert": "Comment Removed."})
