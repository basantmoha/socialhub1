from django.db import models
from django.conf import settings

# Create your models here.
class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'

class passwordReset(models.Model):
    email = models.EmailField()
    reset_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Password reset for {self.email} at {self.created_at}'

class gmail(models.Model):
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Gmail to {self.email} at {self.sent_at}'

def frindship_request_path(instance, filename):
    return f'friendship_requests/user_{instance.from_user.id}/{filename}'

class FriendshipRequest(models.Model):
    
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    attachment = models.FileField(upload_to=frindship_request_path, null=True, blank=True)

    def __str__(self):
        return f'Friendship request from {self.from_user.username} to {self.to_user.username}'
    
class profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_private = models.BooleanField(default=False) 
    pictures = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    def __str__(self):
        return f'Profile of {self.user.username}'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.id}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.id}'
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username} at {self.sent_at}'
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} at {self.created_at}'
    
class privateMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='private_sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='private_received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Private message from {self.sender.username} to {self.recipient.username} at {self.sent_at}'
    
class publication(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Publication: {self.title} by {self.author.username}'
    

