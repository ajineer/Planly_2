from rest_framework import serializers
from ..models.userModel import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User
        fields = ["id", "first_name", "last_name", "email"]
