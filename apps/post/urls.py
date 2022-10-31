from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet,
                    CommentCreateDeleteView,
                    # TagViewSet,
                    LikedPostsView,
                    )   


router = DefaultRouter()
router.register('post', PostViewSet, 'post')
router.register('comment', CommentCreateDeleteView, 'comment')
# router.register('tags', TagViewSet, 'tags')
urlpatterns = [
    path('liked/', LikedPostsView.as_view(), name='liked')
]
urlpatterns += router.urls
