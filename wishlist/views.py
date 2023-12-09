from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Friend_Request, Profile, Wishlist
from .forms import UserCreateForm, UpdateProfileForm, UpdateUserForm, WishlistForm

### Login Stuff ###        #bug where it crashes if failed the first time, then tried again
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
            return redirect("index")
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
    wishlists = Wishlist.objects.all() #edit later
    curr_user = request.user

    if curr_user.id == None:
        return render(request, "wishlist/index.html", {
            'wishlists': wishlists,
            'banner': 'Friends\' Wishlists',
        })

    else:
        return render(request, "wishlist/index.html", {
            'wishlists': wishlists,
            'banner': 'Friends\' Wishlists',
            'wishlist_done': curr_user.wishlist_done,
            'profile_done': curr_user.profile_done
        })
#################

### My Profile ###
@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            message = 'Your profile has been updated successfully'
            return redirect('my_profile', message)
        else:
            return HttpResponseServerError(f'Unknown button clicked')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, "wishlist/edit_profile.html", {
            'user_form': user_form,
            'profile_form': profile_form,
            'banner': 'Edit Profile'
        })
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
        return redirect("index", m='friend request sent')
    else:
        return redirect("index", m='friend request was already sent')

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
    wishlist = request.user.wishlist
    #wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    if request.method == "POST":
        clicked = request.POST["doit"]
        if clicked == "edit-wishlist":
            return redirect('edit-wishlist', wishlist_id=wishlist.id)
        else:
            return HttpResponseServerError(f'Unknown button clicked')
    else:
        return render(request, "wishlist/my_wishlist.html", {
            'wishlist': wishlist,
            'banner': 'My Wishlist',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })

@login_required(login_url='login')
def create_wishlist(request):
    if request.method == "POST":
        if "cancel" in request.POST: 
            return redirect('index')
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.owner = request.user
            request.user.wishlist_done = True
            request.user.save()
            wishlist.save()
            messages.success(request, f'Wishlist created successfully!')
            return redirect("index") 
        else:
            messages.error(request, 'Problem creating the Wishlist. Details below.')
    else:
        form = WishlistForm()
    return render(request, "wishlist/create_wishlist.html", {'form': form})

@login_required(login_url='login')
def edit_wishlist(request):
    wishlist = request.user.wishlist
    wishlist_form = WishlistForm(request.POST, instance=wishlist)
    if request.method == 'POST':
        
        if wishlist_form.is_valid():
            wishlist_form.save()
            #message = 'Your wishlist has been updated successfully'
            return redirect('my-wishlist')
        else:
            return HttpResponseServerError(f'Problem with form')
    else:
        wishlist_form = WishlistForm(request.POST, instance=wishlist)

        return render(request, "wishlist/edit_wishlist.html", {
            'wishlist_form': wishlist_form,
            'banner': 'Edit Wishlist',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })
################

### Secret Santa ###
@login_required(login_url='login')
def secret_santa(request):
    pass
####################