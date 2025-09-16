from rest_framework import serializers
from application.models import CustomUser, FriendshipRequest , Post
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'surname', 'birthdate','password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True, 'required': True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']


class gmailSerializer(serializers.Serializer):
    email = serializers.EmailField()    
    message = serializers.CharField(max_length=500) 
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email must be a Gmail address.")
        return value



class passwordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return value

class passwordcreateSerializer(serializers.Serializer):
    email = serializers.EmailField()    
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return value

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ['id', 'from_user', 'to_user', 'message', 'created_at', 'accepted', 'attachment']
        read_only_fields = ['from_user', 'created_at', 'accepted']

    def validate(self, attrs):
        from_user = self.context['request'].user
        to_user = attrs['to_user']

        if from_user == to_user:
            raise serializers.ValidationError("You cannot send a friendship request to yourself.")
        if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user, accepted=False).exists():
            raise serializers.ValidationError("A pending request already exists.")
        if from_user.friends.filter(id=to_user.id).exists():
            raise serializers.ValidationError("You are already friends.")
        return attrs
    