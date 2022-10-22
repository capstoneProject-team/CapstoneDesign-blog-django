from rest_framework.generics import CreateAPIView, UpdateAPIView ,DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, generics
from .models import Post
from .serializers import PostSerializer



# Create your views here.

class PostListView(generics.ListCreateAPIView) :
    serializer_class = PostSerializer

    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.set_filters(self.get_queryset(), request)

        """
        paginate_queryset 내장 함수에 queryset 객채를 전달한다.
        이때 paginator라는 페이징 클래스를 인스턴스화한 속성에
        size_query_param을 "page_size"를 적용한다.
        이는 한번에 보여줄 게시물의 갯수를 어떤 파라미터를 통해 전달하는지 설정하는 속성이다.
        """
        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)

        """
        page 객체가 존재한다면 get_paginated_response 내장함수를 이용해 응답한다.
        200 Success로 응답한다.
        """
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_filters(self, queryset, request):
        type = request.query_params.get('type', None)
        description = request.query_params.get('description', None)

        if type is not None:
            queryset = queryset.filter(type=type)

        if description is not None:
            queryset = queryset.filter(description__contains=description)

        return queryset


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
