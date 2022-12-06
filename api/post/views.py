from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView

from django.views.generic.detail import DetailView

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from .analyzer import predict

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


class PostDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CreatePostView(CreateAPIView):
    model = Post
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        content = self.request.data.get("content", None)
        keyword = self.request.data.get("keyword", None)
        emotion_list = predict(content)
        serializer.save(
            author=self.request.user,
            happy=emotion_list[0],
            startled=emotion_list[1],
            angry=emotion_list[2],
            anxious=emotion_list[3],
            hurt=emotion_list[4],
            sad=emotion_list[5]
        )



class UpdatePostView(UpdateAPIView) :
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'



class DeletePostView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
