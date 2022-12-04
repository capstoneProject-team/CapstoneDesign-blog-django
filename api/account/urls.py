from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView,TokenRefreshView
from .views import MyTokenObtainPairView

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('edit/pwd/<int:pk>/', views.UpdateInfoView.as_view()),
    path('edit/info/<int:pk>/', views.UpdateInfoView.as_view()),
    path('delete/<int:pk>/', views.DeleteView.as_view()),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('findPassword/', views.FindPasswordView),

]