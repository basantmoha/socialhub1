from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("notifications/", views.notifications_view, name="notifications"),
    path("notifications/mark/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("inbox/", views.inbox, name="inbox"),
    path("inbox/<str:username>/", views.inbox, name="inbox"),
    path('profile/<str:username>/send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('home/', views.home, name='home'),
    path("send-request/<str:username>/", views.send_friend_request, name="send_friend_request"),
    path("friend/<str:username>/", views.friend_profile, name="friend_profile"),
    path("profile/<str:username>/add/", views.add_friend, name="add_friend"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
    path('profile/', views.profile_view, name='my_profile'),    
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('friend/<str:username>/', views.friend_profile, name='friend_profile'),
    path('like/<int:pk>/', views.likeview, name='like_post'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('settings/', login_required(views.user_settings), name='user_settings'),
    path('search/', views.search_friends , name='search_friends'),
    path('logout/', views.logout_view ,name='logout_view'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('password_reset/',
     auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
     name='passreset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name='passreset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name='passreset_confirm'),
    path('password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name='passreset_complete'),
]


