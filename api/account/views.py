import convertapi as convertapi
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer



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



# 회원 삭제
class DeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny
    ]



@api_view(['POST'])
@permission_classes([AllowAny])
def FindPasswordView(request):
    try:
        qs = User.objects.filter(username=request.data['user']['username'],
                                 hint1=request.data['user']['hint1'], hint2=request.data['user']['hint2'])
        serializer = UserSerializer(qs, many=True)
        if(serializer.data[0]==None):
            raise Exception("정보 불일치")
        return Response(serializer.data)
    except Exception as e:
        return HttpResponse('Unauthorized', status=401)


# JWT 토큰 Customizing
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
