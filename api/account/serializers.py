from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   nickname=validated_data['nickname'],
                                   location=validated_data['location'],
                                   ) # 여기에 hint1,2 추가 요망
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model =User
        fields =["pk","username","password","nickname","location"]