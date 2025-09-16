from django.shortcuts import render , redirect
from application.models import Post, CustomUser, FriendshipRequest
from application.api.serializers import UserSerializer , FriendshipRequestSerializer, PostSerializer , gmailSerializer , passwordChangeSerializer , passwordcreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.core.mail import send_mail
from django.contrib.auth import authenticate 
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User # 

from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from django.http import HttpResponse 
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
# like here we can creat and update and delete

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_queryset(self):
        user_name = self.request.query_params.get('username', None)
        if user_name is not None:
            return self.queryset.filter(author__username=user_name) 
        return self.queryset    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   


class gmailAPIView(APIView):
    def post(self, request):
        serializer = gmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            send_mail(
                subject='Subject here',
                message=message,
                from_email='your_email@example.com',
                recipient_list=[email],
                fail_silently=False
                )
            return Response({"detail": "Email sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class passwordChangeAPIView(APIView):
    def post(self, request):
        serializer = passwordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"old_password": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class passwordcreateAPIView(APIView):
    def post(self, request):
        serializer = passwordcreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"email": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def check_conditioncode(code):
    # Dummy condition check function
    return code == "VALID_CODE"


class FriendshipRequestViewSet(ModelViewSet):
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(to_user=self.request.user) | self.queryset.filter(from_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'accepted' in request.data:
            if request.data['accepted'] and not instance.accepted:
                instance.accepted = True
                instance.save()
                return Response({"detail": "Friendship request accepted."}, status=status.HTTP_200_OK)
            elif not request.data['accepted'] and instance.accepted:
                return Response({"detail": "Cannot unaccept a friendship request."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
    
class privateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            profile = user.profile
            if profile.is_private and user != request.user:
                return Response({"detail": "This profile is private."}, status=status.HTTP_403_FORBIDDEN)
            profile_data = {
                "username": user.username,
                "bio": profile.bio,
                "location": profile.location,
                "avatar": profile.avatar.url if profile.avatar else None,
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class get_create_accunt(APIView):
    def post(self, request):
        code = request.data.get('code', '')
        if check_conditioncode(code):
            user = CustomUser.objects.create_user(username='newuser', password='newpassword')
            return Response({"detail": "Account created successfully.", "username": user.username}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)
    # def confirm():
        # if post(request.method=='post'):
        #     return HttpResponse('')
# same feel 
 # nice u solved it
def register(request):
        if request.method == 'POST':
            # process form data
            return redirect('home')  
        return render(request, 'accounts/register.html')