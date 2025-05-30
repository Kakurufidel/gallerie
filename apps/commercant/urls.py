from django.urls import path

from .views import templates_views as views

urlpatterns = [
    # Vues marchand
    path("", views.MerchantDashboardView.as_view(), name="merchant_dashboard"),
    path("profile/", views.MerchantProfileView.as_view(), name="merchant_profile"),
    path("products/", views.ProductListView.as_view(), name="merchant_products"),
    path("products/new/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "products/<int:pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "products/<int:pk>/stock/",
        views.StockManagementView.as_view(),
        name="product_stock",
    ),
    path(
        "transactions/",
        views.TransactionListView.as_view(),
        name="merchant_transactions",
    ),
    # Vues publiques
    path("public/", views.PublicMerchantListView.as_view(), name="public_merchants"),
    path(
        "public/<int:pk>/",
        views.PublicMerchantDetailView.as_view(),
        name="public_merchant_detail",
    ),
    path(
        "public/products/<int:pk>/",
        views.PublicProductDetailView.as_view(),
        name="public_product_detail",
    ),
]
