from django.urls import path
from users.views.api_views import (MerchantActivationAPIView,
                                   MerchantListAPIView, UserCreateAPIView,
                                   UserDetailAPIView, UserListAPIView,
                                   UserLoginAPIView, UserProfileAPIView)

app_name = "users_api"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    # Users management (admin only)
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    # Merchants
    path("merchants/", MerchantListAPIView.as_view(), name="merchant-list"),
    path(
        "merchants/<int:pk>/activate/",
        MerchantActivationAPIView.as_view(),
        name="merchant-activate",
    ),
]
