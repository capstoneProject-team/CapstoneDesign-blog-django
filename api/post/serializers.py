from django.contrib.auth import get_user_model
from rest_framework import serializers
from . models import Post
# from .analyzer import predict


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "photo", "content", "created_at", "updated_at",
            "happy", "angry", "hurt", "startled", "anxious", "sad", "keyword"
        ]


    author = serializers.SerializerMethodField("get_author_nickname")
    keyword = serializers.SerializerMethodField("get_emotions_keyword")


    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_emotions_keyword(self, obj):
        content = obj.content
        # return predict(content)
        return content


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance



class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "photo", "content", "created_at", "updated_at",
            "happy", "angry", "hurt", "startled", "anxious", "sad", "keyword"
        ]

    author = serializers.SerializerMethodField("get_author_nickname")

    def get_author_nickname(self, obj):
        return obj.author.nickname

