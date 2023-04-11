from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
            "role",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": ("Данная почта уже используется.")}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "password"]


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "role",
        ]

    def update(self, instance, validated_data):
        validated_data.pop("password", None)  # exclude password field
        return super().update(instance, validated_data)
