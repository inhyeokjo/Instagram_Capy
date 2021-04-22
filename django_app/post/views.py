from post.serializers import PostListSerializer, PostDetailSerializer, CommentListSerializer, CommentDetailSerializer
from post.models import Post, Comment
from instagram_app import permissions as up
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

class PostListCreate(generics.ListCreateAPIView):
    permission_classes = (
        up.IsMethodGet |
        up.IsMethodPost & permissions.IsAuthenticated,
    )

    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return super().get_serializer(*args, **kwargs)
        copy_trick = kwargs['data'].copy()
        copy_trick.update(user=self.request.user.id)
        kwargs['data'] = copy_trick
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class PostDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        up.IsMethodGet |
        (up.IsMethodDelete | up.IsMethodPatch) & permissions.IsAuthenticated,
    )
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'


class CommentCreateList(generics.ListCreateAPIView):
    permission_classes = (
        up.IsMethodGet |
        up.IsMethodPost & permissions.IsAuthenticated,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        data_copy.update(post=kwargs['related_id'])
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return super().get_serializer(*args, **kwargs)
        copy_trick = kwargs['data'].copy()
        copy_trick.update(user=self.request.user.id)
        kwargs['data'] = copy_trick
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CommentDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        up.IsMethodGet |
        ((up.IsMethodDelete | up.IsMethodPatch) & permissions.IsAuthenticated),
    )
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
