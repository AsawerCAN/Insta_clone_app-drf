from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from insta_app.models import Post, PostComment, PostLike, User, UserFollow

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField()
    bio = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "bio")  # Consider read-only fields

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(validated_data['email'], password=password)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Read-only user field

    class Meta:
        model = Post
        fields = ("id", "title", "description", "user", "created_at", "updated_at")

    def update(self, instance, validated_data):
            print(validated_data)
            if instance.user.id == validated_data["user"].id:
                return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Read-only user field
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PostComment
        fields = ("id", "comment_text", "user", "post", "created_at", "updated_at")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['post'] = PostSerializer(instance.post).data  # Optional: Nested post data
        return response


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PostLike
        fields = "__all__"  # Change to `fields = ('user', 'post')` if read-only


class UserFollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follows_id = serializers.PrimaryKeyRelatedField(source='follows', read_only=True)

    class Meta:
        model = UserFollow
        fields = ("user", "follows_id")
