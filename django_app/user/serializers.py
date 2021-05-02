from rest_framework import serializers
from user import models


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'username',
            'password',
            'name',
            'description',
            'profile_image'
        ]