from rest_framework import serializers
from ..models.userModel import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User
        fields = ["id", "first_name", "last_name", "email", "is_active"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
