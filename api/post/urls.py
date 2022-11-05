from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('post', views.PostViewSet)

urlpatterns = [
    path('', views.PostListView.as_view()),
    path('', views.PostDetailView.as_view()),
    path('create/', views.CreatePostView.as_view()),
    path('update/<int:pk>/', views.UpdatePostView.as_view()),
    path('delete/<int:pk>/', views.DeletePostView.as_view()),
]