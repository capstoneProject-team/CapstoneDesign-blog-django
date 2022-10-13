from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   nickname=validated_data['nickname'],
                                   location=validated_data['location'],
                                   )  # 여기에 hint1,2 추가 요망
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance



    class Meta:
        model = User
        fields = ["id", "username", "password", "nickname", "location"]
