from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User, Friend_Request
from .forms import UserCreateForm

### Login Stuff ###
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "index")
            return redirect(next_url)
        else:
            return render(request, "wishlist/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next_url = request.GET.get("next", "index")
        return render(request, "wishlist/login.html", {"next": next_url })


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return HttpResponse('LoggedIn') #redirect("index")
        else:
            print(request.POST, form.errors)
            return render(request, "wishlist/register.html", {
                'form': form, 'error': form.errors
            })
    else:
        form = UserCreateForm()
        return render(request, "wishlist/register.html", {'form': form})
###################

### Home Page ###
def index(request):
    return render(request, "wishlist/index.html", {
        'banner': 'Friends\' Wistlists'
    })
#################

### My Profile ###
@login_required(login_url='login')
def my_profile(request):
    pass
##################

### Friend Requests ###
@login_required(login_url='login')
def add_friend(request):
    pass

@login_required(login_url='login')
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        redirect("index", m='friend request sent')
    else:
        redirect("index", m='friend request was already sent')

@login_required(login_url='login')
def accept_friend_request(request, request_id):
    friend_request = Friend_Request.objects.get(id=request.ID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')
#######################

### Wishlist ###
@login_required(login_url='login')
def my_wishlist(request):
    pass
################

### Secret Santa ###
@login_required(login_url='login')
def secret_santa(request):
    pass
####################