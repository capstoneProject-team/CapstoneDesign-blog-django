from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import  MyTokenObtainPairSerializer


#Create your views here.

# 회원가입
class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny
    ]


# 회원정보 수정
class UpdateInfoView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "User Info updated successfully"})
    #     else:
    #         return Response({"message": "failed", "details": serializer.errors})


class DeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
