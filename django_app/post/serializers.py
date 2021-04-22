from rest_framework import serializers
from post import models


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['user',
                  'id',
                  'body',
                  'created_at']
        extra_kwargs = {
            'body': {'write_only': True}
        }


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id',
                  'user',
                  'body',
                  'created_at']
        read_only_fields = ['user']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['user',
                  'post',
                  'mother',
                  'body',
                  'created_at',
                  'id']
        extra_kwargs = {
            'body': {'write_only': True},
        }


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['user',
                  'post',
                  'mother',
                  'body',
                  'created_at',
                  'id']
        read_only_fields = ['user']

