from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


from .models import User, Profile, Wishlist

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    fname = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    birthday = forms.DateField(widget=forms.DateField())

    class Meta:
        model = Profile
        fields = ['avatar', 'fname']

class WishlistForm(forms.ModelForm):

    class Meta:
        model = Wishlist
        fields = ('fav_color', 'fav_food', 'fav_drink', 'fav_candy', 'fav_animal', 'fav_media', 'fav_hobby', 'fav_book', 'fav_game', 'fav_music', 'gift_ideas')
        labels = {
            'fav_color': "Favorite color", 
            'fav_food': "Favorite food", 
            'fav_drink': "Favorite drink", 
            'fav_candy': "Favorite candy", 
            'fav_animal': "Favorite animal", 
            'fav_media': "Favorite movie/tv/anime", 
            'fav_hobby': "Favorite hobby", 
            'fav_book': "Favorite book", 
            'fav_game': "Favorite game", 
            'fav_music': "Favorite music artist", 
            'gift_ideas': "Gift ideas"
        }