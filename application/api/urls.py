from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet , PostViewSet , gmailAPIView , passwordChangeAPIView , passwordcreateAPIView , FriendshipRequestViewSet , get_create_accunt , register

from . import views
from application.api import views

router = DefaultRouter()
router.register(r'users', UserViewSet) 
urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', views.register, name='register'),
    path('api/password_reset/', views.passwordChangeSerializer, name='password_reset'),
    path('api/password_reset/done/',views.passwordcreateSerializer,name='password_reset_done'),
    path('api/create_post/', PostViewSet.as_view({'post': 'create'}), name='create_post'),
    path('api/home/',register, name='home'),
]  
    
# there is error in the line 9 please fix it
#TypeError: passwordcreateAPIView() received an invalid keyword 'template_name'. as_view only accepts arguments that are already attributes of the class.
