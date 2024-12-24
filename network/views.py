import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import User, Post, Follow

paginateby = 10


def index(request):
    allpost = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(allpost, paginateby)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


@login_required
def newpost(request):
    if request.method == 'POST':
        postcontent = request.POST['newpost']
        newpsot = Post.objects.create(
            poster=request.user,
            content=postcontent,
        )
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def like(request, post_id):

    if request.method == 'PUT':
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)

        if data.get('like') is not None:
            if data['like']:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            post.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error":"something went wrong"})
    else:
        return JsonResponse({
            "message": "mission successfull",
        })


def viewuser(request, user_id):
    allpost = Post.objects.filter(poster=user_id).order_by('-timestamp')
    user = User.objects.get(pk=user_id)

    follower = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)


    followerslist = []
    print('followers: ')
    for person in follower:
        print(person)
        followerslist.append(person.follower)

    print(f'followerlist: {followerslist}')

    followinglist = []
    print('following: ')
    for person in following:
        print(person)
        followinglist.append(person.following)

    print(f'followinglist: {followinglist}')
    


    paginator = Paginator(allpost, paginateby)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/user.html',{
        'page_obj': page_obj,
        'numfollower': len(followerslist),
        'numfollowing': len(followinglist),
        'followers': followerslist,
        'followings': followinglist,
        'userpage': user
    })


@csrf_exempt
@login_required
def follow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('whowantstofollow') is not None:
            followerid = data['whowantstofollow']
        if data.get('targetfollow') is not None:
            targetfollowingid = data['targetfollow']
        
        follower = User.objects.get(pk=followerid)
        targetfollowing = User.objects.get(pk=targetfollowingid)

        Follow.objects.create(
            follower=follower,
            following=targetfollowing
        )

        return HttpResponse(status=204)
    else:
        return JsonResponse({
            'message': 'following'
        })
    

@csrf_exempt
@login_required
def unfollow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('whowantstounfollow') is not None:
            unfollowerid = data['whowantstounfollow']
        if data.get('targetunfollow') is not None:
            targetunfollowingid = data['targetunfollow']
        
        unfollower = User.objects.get(pk=unfollowerid)
        targetunfollowing = User.objects.get(pk=targetunfollowingid)

        try:
            followobject = Follow.objects.get(
                follower=unfollower,
                following=targetunfollowing
            )
            followobject.delete()
        except Follow.DoesNotExist:
            return JsonResponse({
                "error": "does not exist"
            })

        return HttpResponse(status=204)
    else:
        return JsonResponse({
            'message': 'unfollowing'
        })


@login_required
def following(request):
    allpost = Post.objects.all().order_by('-timestamp')
    followings = Follow.objects.filter(follower=request.user)

    followinglist = []
    print('following: ')
    for person in followings:
        # print(person)
        followinglist.append(person.following)

    print(f'followinglist: {followinglist}')


    followingpost = []
    for post in allpost:
        if post.poster in followinglist:
            print(post)
            followingpost.append(post)
        else:
            print('not it following')

    paginator = Paginator(followingpost, paginateby)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html',{
        'page_obj': page_obj,
        'following': followinglist
    })

@csrf_exempt
@login_required
def saveeditpost(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('content') is not None:
            newcontent = data['content']
        
        post.content = newcontent
        post.save()

        return JsonResponse({
            'message': 'edit saved successfully'
        })
    else:
        return JsonResponse({
            "message": "complete novels"
        }, safe=False)


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
