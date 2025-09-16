from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post, Comment , FriendRequest ,Notification
from .forms import ProfileUpdateForm, UserSettingsForm 
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.conf import settings as django_settings
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from django.contrib import messages as django_messages
from .models import Message


@login_required
def home(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        privacy = request.POST.get('privacy', 'public')
        if content or image: 
             Post.objects.create(user=request.user, content=content, image=image, privacy=privacy)
        else:
             messages.error(request, "You cannot create an empty post.")
        return redirect('home')
    posts = Post.objects.filter(privacy='public')
    user_profile = request.user.profile
    friends_ids = user_profile.friends.values_list('id', flat=True)
    private_friend_posts = Post.objects.filter(user__id__in=friends_ids, privacy='private')
    my_posts = Post.objects.filter(user=request.user)
    posts = (posts | private_friend_posts | my_posts).order_by('-created_at')
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'user/home.html', {'posts': posts ,'unread_count': unread_count})


@login_required
def likeview(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if request.user != post.user:  
            Notification.objects.create(
                user=post.user,  
                message=f"{request.user.username} liked your post."  
            )
            try:
                send_mail(
                    subject='Someone liked your post!',
                    message=f'Hi {post.user.first_name},\n\n{request.user.username} liked your post.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[post.user.email],
                    fail_silently=False,
                )
            except:
                pass 
    return redirect('home')



def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            Comment.objects.create(
                user=request.user,
                post=post,
                body=body 
            )
            if request.user != post.user:
                Notification.objects.create(
                    user=post.user,
                    message=f"{request.user.username} commented on your post."
                )
                try:
                    send_mail(
                        subject='New comment on your post!',
                        message=f'Hi {post.user.first_name},\n\n{request.user.username} commented: "{body}"',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[post.user.email],
                        fail_silently=False,
                    )
                except:
                    pass
    return redirect("home")


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'user/edit_profile.html', {'form': form})


@login_required
def profile_view(request, username=None):
    if username:
        user_profile = get_object_or_404(User, username=username)
    else:
        user_profile = request.user
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')
    context = {
        'user_profile': user_profile,
        'posts': posts,
        'full_name': f"{user_profile.first_name} {user_profile.last_name}" 
    }
    return render(request, 'user/profile.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(user=request.user, content=content, image=image)
        return redirect('home')  
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'user/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        sur_name = request.POST.get('surname') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password != confirmpassword:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        if User.objects.filter(email= email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=sur_name,
            email=email,
            password=password
        )
        Profile.objects.create(user=user, first_name=first_name, last_name=sur_name)
        login(request, user)
        try:
            send_mail(
                subject='Welcome to facebook 🎉',
                message=f'Hi {first_name} {sur_name},\nThank you for registering!',
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except:
            messages.warning(request, 'Account created but email failed.')
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    return render(request, 'registration/register.html')

@login_required
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")  
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, "registration/login.html")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "registration/login.html")
    return render(request, "registration/login.html")


@login_required
def user_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  
            request.session[settings.LANGUAGE_COOKIE_NAME] = form.cleaned_data['language']
            return redirect('user_settings')
    form = UserSettingsForm(instance=profile)
    return render(request, 'user/settings.html', {'form': form})

    
def search_friends(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    return render(request, 'user/search_results.html', {'results': results, 'query': query})

@login_required
def profile_detail(request, username):
    user_obj = get_object_or_404(User, username=username)
    user_profile, _ = Profile.objects.get_or_create(user=user_obj)
    current_user_profile = request.user.profile
    is_friend = current_user_profile.friends.filter(id=user_obj.id).exists()
    request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user_obj, is_accepted=False).first()
    request_received = FriendRequest.objects.filter(from_user=user_obj, to_user=request.user, is_accepted=False).first()
    if user_profile.privacy == "private" and not is_friend:
        posts = []
    else:
        posts = Post.objects.filter(user=user_obj).order_by('-created_at')
    if request.method == "POST":
        if "add_friend" in request.POST:
            if user_profile.privacy == "private" and not is_friend:
                current_user_profile.friends.add(user_obj)
                user_profile.friends.add(request.user)
                messages.success(request, f"You are now friends with {user_obj.username}")
            else:
                if not request_sent:
                    FriendRequest.objects.create(from_user=request.user, to_user=user_obj)
                    messages.info(request, f"Friend request sent to {user_obj.username}")
        elif "accept_friend" in request.POST:
            if request_received:
                request_received.is_accepted = True
                request_received.save()
                current_user_profile.friends.add(user_obj)
                user_profile.friends.add(request.user)
                messages.success(request, f"You are now friends with {user_obj.username}")
        elif "remove_friend" in request.POST:
            if is_friend:
                current_user_profile.friends.remove(user_obj)
                user_profile.friends.remove(request.user)
                messages.success(request, f"You removed {user_obj.username} from your friends.")
        return redirect("profile_detail", username=username)

    return render(request, "user/profile_detail.html", {
        "user_profile": user_obj,
        "is_friend": is_friend,
        "request_sent": request_sent,
        "request_received": request_received,
        "posts": posts,
    })

@login_required
def notifications_view(request):
    notifications = request.user.notifications.order_by("-timestamp")
    friend_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    return render(request, "user/notifications.html", {
        "notifications": notifications,
        "friend_requests": friend_requests
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name  
        user_email = request.user.email
        logout(request)  
        send_mail(
            subject="Goodbye from OurSite!",
            message=f"Thank you {first_name} for visiting our site. You have successfully logged out.",
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        messages.success(request, f"Thank you {first_name}! A logout email has been sent to {user_email}.")
        messages.success(request, f"Thank you {first_name}!")
    return redirect('login')

@login_required
def friend_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    has_sent_request = request.user.sent_requests.filter(to_user=user_profile).exists()
    has_received_request = user_profile.sent_requests.filter(to_user=request.user).exists()
    return render(request, "user/profile_detail.html", {
        "user_profile": user_profile,
        "has_sent_request": has_sent_request,
        "has_received_request": has_received_request,
    })


@login_required
def reject_friend_request(request, request_id):
    first_name = request.user.first_name  
    user_email = request.user.email
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    send_mail(
            subject="Friendship rejected.",
            message=f"User {first_name} rejected your friend request.",
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
    messages.info(request, "Friend request rejected.")
    return redirect("notifications")

@login_required
def add_friend(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = request.user.profile 
    target_profile = target_user.profile 
    if profile.friends.filter(id=target_user.id).exists():
        messages.warning(request, f"You are already friends with {target_user.username}.")
    else:
        profile.friends.add(target_user)
        target_profile.friends.add(request.user)
        messages.success(request, f"You are now friends with {target_user.username}.")

    return redirect("profile_detail", username=username)


@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    current_user_profile = request.user.profile
    to_user_profile = to_user.profile
    if to_user == request.user:
        messages.error(request, "You cannot send a request to yourself.")
        return redirect("profile_detail", username=username)
    existing_request = FriendRequest.objects.filter(from_user=to_user, to_user=request.user, is_accepted=False).first()
    if existing_request:
        existing_request.is_accepted = True
        existing_request.save()
        current_user_profile.friends.add(to_user)
        to_user_profile.friends.add(request.user)
        messages.success(request, f"You are now friends with {to_user.username}")
    else:
        if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user, is_accepted=False).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            messages.info(request, f"Friend request sent to {to_user.username}")
        else:
            messages.info(request, "You already sent a friend request.")
    Notification.objects.create(
    user=to_user, 
    sender=request.user, 
    message=f"{request.user.username} sent you a friend request."
    )
    return redirect("profile_detail", username=username)

@login_required
def inbox(request, username=None):
    user_profile = request.user.profile
    friends = user_profile.friends.all()  
    chat_user = None
    messages_thread = []

    if username:
        chat_user = get_object_or_404(User, username=username)

        if chat_user in friends:
            messages_thread = Message.objects.filter(
                Q(sender=request.user, receiver=chat_user) |
                Q(sender=chat_user, receiver=request.user)
            ).order_by("timestamp")

            if request.method == "POST":
                content = request.POST.get("content", "").strip()
                image = request.FILES.get("image")

                if content or image:
                    msg = Message.objects.create(
                    sender=request.user,
                    receiver=chat_user,
                    content=content,
                    image=image if image else None,
                    )
                    msg.is_read = False  
                    msg.save()
                    if request.user != chat_user:
                        Notification.objects.create(
                            user=chat_user,
                            message=f"{request.user.username} sent you a message."
                        )

                    return redirect("inbox", username=chat_user.username)
    return render(request, "user/inbox.html", {
        "friends": friends,
        "chat_user": chat_user,
        "messages_thread": messages_thread,
    })
