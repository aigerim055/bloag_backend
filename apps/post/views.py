from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# from rest_framework.generics import ( 
#     ListAPIView, 
#     RetrieveAPIView, 
#     DestroyAPIView, 
#     UpdateAPIView, 
#     CreateAPIView
# )

from .models import (
    Post,
    Tag,
    Comment,
)
from .serializers import (
    PostListSerializer,
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
)

from .permissions import IsOwner

# class PostListView(ListAPIView):
#     # quearyset = Post.objects.filter(status='open')
#     quareyset = Post.objects.all()
#     serializer_class = PostListSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes == [IsOwner]
        if self.action in ['create', 'comment']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request,pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        comment = Comment.objects.filter(
            user=request.user,
            post=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user, post=post)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            elif comment is not None and request.method == 'DELETE':
                comment.delete()
                return Response(
                    'deleted!',
                    status=status.HTTP_204_NO_CONTENT
                )


class CommentCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




"""  
actions
create() - POST
retrieve() - GET /post/1/
list() - GET /post/
destroy() - DELETE /post/1/
partial_update() - PATCH /post/1/
update() - PUT /post/1/
"""

# TODO: поправить удаление комментариев
# TODO: создание лайков
# TODO: отображение лайков в постах
# TODO: создать модельку рейтингов
# TODO: создание рейтинга и отображение в постах
