from dataclasses import field, fields
from email.policy import default
from xml.dom import ValidationErr
from rest_framework import serializers
from django.db.models import Avg
from .models import(
    Post,
    Tag,
    Rating,
    Comment,
    PostImage,
    Like,
)


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'title', 'image', 'slug')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = '__all__'

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        representation['carousel'] = PostImageSerializer(
            instance.post_images.all(), many=True
        ).data
        rating = instance.ratings.aggregate(Avg('rating'),)['rating__avg']
        representation['likes'] = instance.likes.all().count()
        representation['liked_by'] = LikeSerializer(instance.likes.all().only('user'), many=True).data
        if rating:
            representation['rating'] = round(rating,1)
        else:
            representation['rating'] = 0.0
        return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = 'image',


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ('tag',)

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        tag = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        post.tag.set(tag)
        images = []
        for image in carousel_images:
            images.append(PostImage(post=post, image=image))
        PostImage.objects.bulk_create(images)
        return  post

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        exclude = ['post']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = Rating
        fields = ('rating', 'user', 'post')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('wrong value! rating must be between 1 and 5')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, attrs):
        tag = attrs.get('title')
        if Tag.objects.filter(title=tag).exists():
            raise serializers.ValidationError('tag with this name already exists')
        return attrs


class CurrentPostDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['post']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.HiddenField(default=CurrentPostDefault())
    

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        post = self.context.get('post').pk
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            raise serializers.ValidationError('already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        post = self.context.get('post').pk
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('not liked yet')


class LikedPostsSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='post.get_absolute_url')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Like
        fields = ['post', 'user', 'url']