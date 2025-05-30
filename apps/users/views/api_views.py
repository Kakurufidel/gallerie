from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.api.serializers import (MerchantActivationSerializer,
                                   UserCreateSerializer, UserLoginSerializer,
                                   UserSerializer)
from users.models import User


class UserCreateAPIView(APIView):
    """Endpoint for user registration"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            "user": UserSerializer(user).data,
            "message": _("User created successfully"),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    """Endpoint for user login (JWT token generation)"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data,
            }
        )


class UserProfileAPIView(APIView):
    """Endpoint for user profile management"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    """Endpoint for listing users (admin only)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailAPIView(APIView):
    """Endpoint for user details (admin only)"""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MerchantActivationAPIView(APIView):
    """Endpoint for merchant account activation (admin only)"""

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        merchant = get_object_or_404(User.objects.filter(role="MERCHANT"), pk=pk)
        serializer = MerchantActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        merchant.is_verified = serializer.validated_data["is_verified"]
        merchant.save(update_fields=["is_verified"])

        return Response(
            {"status": _("Merchant verification status updated")},
            status=status.HTTP_200_OK,
        )


class MerchantListAPIView(generics.ListAPIView):
    """Endpoint for listing merchants"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role="MERCHANT")
