
import requests
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
                                   hint1=validated_data['hint1'],
                                   hint2=validated_data['hint2'],
                                   question1=validated_data['question1'],
                                   question2=validated_data['question2'],
                                   question3=validated_data['question3'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if(validated_data.get('nickname')==None):
            instance.set_password(validated_data.get('password'))
            instance.save()
        else:
            instance.nickname = validated_data.get('nickname', instance.nickname)
            instance.save()

        return instance

    class Meta:
        model = User
        fields = ["id", "username", "password", "nickname", "location",
                  "hint1", "hint2", "question1", "question2", "question3"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname']=str(user.nickname)
        token['location']=str(user.location)
        token['email']=user.username

        return token