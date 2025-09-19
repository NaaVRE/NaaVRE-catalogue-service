from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='last_name')

    class Meta:
        model = User

        fields = [
            'username',
            'name',
            ]
