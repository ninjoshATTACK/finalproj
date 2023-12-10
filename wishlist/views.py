from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Friend_Request, Profile, Wishlist
from .forms import UserCreateForm, UpdateProfileForm, UpdateUserForm, WishlistForm, SearchForm

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
        friends = request.user.friends.all()
        return render(request, "wishlist/index.html", {
            'wishlists': wishlists,
            'banner': 'Friends\' Wishlists',
            'wishlist_done': curr_user.wishlist_done,
            'profile_done': curr_user.profile_done,
            'friends': friends
        })
#################

### My Profile ###
@login_required(login_url='login')
def create_profile(request):
    if request.method == 'POST':
        if "cancel" in request.POST: 
            return redirect('index')
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            request.user.profile_done = True
            request.user.save()
            profile.save()
            messages.success(request, f'Congratulations on finishing your profile!')
            return redirect("index") 
        else:
            messages.error(request, 'Problem creating the Wishlist. Details below.')
    else:
        form = UpdateProfileForm()

        return render(request, "wishlist/create_profile.html", {
            'profile_form': form,
            'banner': 'Create Profile',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            message = 'Your profile has been updated successfully'
            return redirect('index')
        else:
            return HttpResponseServerError(f'Unknown button clicked')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, "wishlist/edit_profile.html", {
            'user_form': user_form,
            'profile_form': profile_form,
            'banner': 'Edit Profile',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })
##################

### Friend Requests ###
@login_required(login_url='login')
def add_friend(request, user_id):
    friend = User.objects.get(id=user_id)
    if friend.profile_done == False:
        return render(request, "wishlist/add_friend.html", {
            'friend': friend,
            'banner': 'Profile',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })
    else:
        p = friend.profile
        return render(request, "wishlist/add_friend.html", {
            'friend': friend,
            'profile': p,
            'banner': 'Profile',
            'wishlist_done': request.user.wishlist_done,
            'profile_done': request.user.profile_done
        })

@login_required(login_url='login')
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        messages.success(request, f'friend request sent')
        return redirect("index")
    else:
        messages.error(request, f'friend request sent')
        return redirect("index")

@login_required(login_url='login')
def accept_friend_request(request, request_id):
    friend_request = Friend_Request.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, f'friend accepted')
        return redirect('index')
    else:
        messages.success(request, f'friend request not accepted')
        return redirect('index')
    
@login_required(login_url='login')
def search_for_friend(request):
    if request.method == "GET":
        q = request.GET.get("q","")

        if q != "":
            showfriend = False
            for u in User.objects.all():
                # User was found
                if q.lower() == u.username.lower():
                    friend_id = u.id
                    showfriend = True
                    break
            # Display result if found
            if showfriend:
                messages.success(request, f'Username found')
                return redirect('add-friend', user_id=friend_id)
            else:
                results = []
                for u in User.objects.all():
                    #To see if substring is found
                    if q.lower() in u.username.lower():
                        results.append(u)
                # User was not found
                if len(results) == 0:
                    form = SearchForm()
                    m = "The username you searched doesn't exist"
                    return render(request, "wishlist/search_for_friend.html", {
                        'form': form, 
                        'message': m,
                        'wishlist_done': request.user.wishlist_done,
                        'profile_done': request.user.profile_done
                    })
                # The substring was found within these users
                else:
                    return render(request, "wishlist/search_for_friend.html", {
                        "results": results,
                        "form": q,
                        'wishlist_done': request.user.wishlist_done,
                        'profile_done': request.user.profile_done
                    })
        else:
            form = SearchForm()
            m = "No users found"
            frequests = Friend_Request.objects.all().filter(to_user=request.user)
            return render(request, "wishlist/search_for_friend.html", {
                'all_friend_requests': frequests,
                'form': form,
                'm': m,
                'wishlist_done': request.user.wishlist_done,
                'profile_done': request.user.profile_done
            })
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