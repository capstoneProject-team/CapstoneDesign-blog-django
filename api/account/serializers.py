from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        saveInstance = instance
        saveInstance.username = validated_data.get('username', instance.username)
        saveInstance.set_password(validated_data.get('password', instance.password))
        saveInstance.nickname = validated_data.get('nickname', instance.nickname)
        saveInstance.location = validated_data.get('location', instance.location)
        saveInstance.save()
        return saveInstance



    class Meta:
        model = User
        fields = ["id", "username", "password", "nickname", "location"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nickname']=user.nickname
        token['location']=user.location
        token['email']=user.username

        return token