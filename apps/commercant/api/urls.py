from django.urls import path

from apps.commercant.views.api_views import (
    MerchantAPIView,
    MerchantDetailAPIView,
    ProductAPIView,
    ProductStockAPIView,
    TransactionAPIView,
)

app_name = "commercant_api"

urlpatterns = [
    # Merchants
    path("", MerchantAPIView.as_view(), name="merchants-list"),
    path("<int:pk>/", MerchantDetailAPIView.as_view(), name="merchant-detail"),
    # Products
    path(
        "<int:merchant_pk>/products/",
        ProductAPIView.as_view(),
        name="merchant-products",
    ),
    path(
        "products/<int:product_pk>/stock/",
        ProductStockAPIView.as_view(),
        name="product-stock",
    ),
    # Transactions
    path("transactions/", TransactionAPIView.as_view(), name="transactions-list"),
    path(
        "products/<int:product_pk>/transactions/",
        TransactionAPIView.as_view(),
        name="product-transactions",
    ),
]
