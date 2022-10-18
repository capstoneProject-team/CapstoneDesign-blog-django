from django.shortcuts import render
from rest_framework.decorators import authentication_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, generics
from .models import Post
from .serializers import PostSerializer



# Create your views here.

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    model = Post
    # paginate_by = 5
    # def get_queryset(self):
    #     post_id = self.kwargs['poster_id']
    #     queryset = self.model.objects.filter(poster_id=poster_id)
    #     return queryset.order_by('-post_time')

class CreatePostView(CreateAPIView):

    model = Post
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdatePostView(UpdateAPIView) :
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'


class DeletePostView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
