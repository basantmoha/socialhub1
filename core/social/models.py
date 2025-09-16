from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    privacy = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    email_notifications = models.BooleanField(default=True)
    theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ar', 'Arabic')], default='en')
    @staticmethod
    def friend_count(user):
        return FriendRequest.objects.filter(from_user=user, is_accepted=True).count() + \
            FriendRequest.objects.filter(to_user=user, is_accepted=True).count()
    def __str__(self):
        return self.user.username

class Post(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    privacy = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private'),(('friends', 'Friends Only'))], default='public')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Title')
    content = models.TextField()
    image = models.ImageField(upload_to='post/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='BLOG_POSTS')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class Comment(models.Model): 
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    language = models.CharField(max_length=5, 
        choices=[
            ('en', 'English'),
            ('ar', 'Arabic')
        ],
        default='en'
    )
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="messages/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"] 
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
       
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"