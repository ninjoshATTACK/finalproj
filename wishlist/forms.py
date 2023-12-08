from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


from .models import User, Profile

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
        fields = ['avatar', 'fname', 'birthday']