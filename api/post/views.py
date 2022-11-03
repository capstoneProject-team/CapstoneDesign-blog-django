from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView
from django.views.generic.detail import DetailView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, generics
from .models import Post
from .serializers import PostSerializer
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

# Create your views here.

class PostListView(generics.ListCreateAPIView) :
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        author_id = self.request.GET.get('author_id')
        queryset = Post.objects.filter(author_id=author_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.set_filters(self.get_queryset(), request)

        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_filters(self, queryset, request):
        title = request.query_params.get('title', None)
        content = request.query_params.get('content', None)
        created_at = request.query_params.get('created_at', None)

        if title is not None:
            queryset = queryset.filter(title__contains=title)

        if content is not None:
            queryset = queryset.filter(content__contains=content)

        if created_at is not None:
            queryset = queryset.filter(created_at__contains=created_at)

        return queryset


class PostDetailView(DetailView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.request.GET.get('post_id')
        queryset = Post.objects.filter(post_id=post_id)
        return queryset


class CreatePostView(CreateAPIView):
    model = Post
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class UpdatePostView(UpdateAPIView) :

    def get_queryset(self):
        author_id = self.request.GET.get('author_id')
        queryset = Post.objects.filter(author_id=author_id)
        return queryset

    serializer_class = PostSerializer
    lookup_field = 'pk'


class DeletePostView(DestroyAPIView):
    def get_queryset(self):
        author_id = self.request.GET.get('author_id')
        queryset = Post.objects.filter(author_id=author_id)
        return queryset

    serializer_class = PostSerializer
