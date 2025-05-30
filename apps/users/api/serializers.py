from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "role",
            "is_verified",
            "last_activity",
            "date_joined",
        ]
        read_only_fields = ["id", "is_verified", "last_activity", "date_joined"]
        extra_kwargs = {"email": {"required": True}, "phone": {"required": False}}

    def validate(self, attrs):
        if attrs.get("role") == "MERCHANT" and not attrs.get("phone"):
            raise serializers.ValidationError(
                _("Merchants must provide a phone number")
            )
        return attrs


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}, "role": {"default": "CLIENT"}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone"),
            birth_date=validated_data.get("birth_date"),
            role=validated_data.get("role", "CLIENT"),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class MerchantActivationSerializer(serializers.Serializer):
    is_verified = serializers.BooleanField(required=True)
