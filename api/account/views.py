import json
import bcrypt

from .models import User

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from decouple import config

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.
# 회원가입
class SignUp(View):
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def signUp(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "EXISTS_EMAIL"}, status=400)

            User.objects.create(
                email = data['email'],
                password = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            ).save()
                
            return HttpResponse(status=200)
            
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status=400)


# # 로그인
# def logIn(self, request):
#     data = json.loads(request.body)

#     try:
#         if Account.objects.filter(email=data["email"]).exists():
#             user = Account.objects.get(email=data["email"])

#             if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
#                 payload_value = user.id
#                 payload = {
#                     "subject" : payload_value,
#                 }
#                 token = generate_token(payload, "access")
#                 return JsonResponse({"token": token}, status=200)

#             return HttpResponse(status=401)

#         return HttpResponse(status=400)
        
#     except KeyError:
#         return JsonResponse({'message' : "INVALID_KEYS"}, status=400)

