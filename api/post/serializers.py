from django.contrib.auth import get_user_model
from rest_framework import serializers
from . models import Post

# class PostSerializer(serializers.ModelSerializer):
#
#     def create(self, validated_data):
#         post = Post.objects.create(author=validated_data['author'],
#                                    content=validated_data['content'],
#                                    photo=validated_data['photo'],
#                                    created_at=validated_data['created_at'],
#                                    )
#         post.save()
#         return post
#
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.photo = validated_data.get('photo', instance.photo)
#         instance.save()
#         return instance
#
#     author = serializers.SerializerMethodField("get_user_nickname")
#
#     def get_user_nickname(self, obj):
#         return obj.user.nickname
#
#     class Meta:
#         model = Post
#         fields = ["id", "author", "title", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "photo",
            "content",
            "created_at",
            "updated_at",
        ]

    author = serializers.SerializerMethodField("get_author_nickname")

    def get_author_nickname(self, obj):
        return obj.author.nickname


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "photo",
            "content",
            "created_at",
            "updated_at",
        ]

    author_email = serializers.SerializerMethodField("get_author_nickname")

    def get_author_nickname(self, obj):
        return obj.author.nickname