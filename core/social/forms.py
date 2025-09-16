from django import forms
from .models import Profile, Post , UserSetting
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
from .models import UserSetting
from .models import FriendRequest
from .models import Message

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_pic']

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'privacy']  

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['privacy', 'email_notifications', 'theme', 'language']
        widgets = {
            'privacy': forms.RadioSelect(),
            'email_notifications': forms.CheckboxInput(),
            'theme': forms.Select(),
            'language': forms.Select(),
        }
        
class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic'] 

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = []
