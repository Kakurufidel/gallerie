from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.commercant.api.serializer import (
    MerchantDetailSerializer,
    MerchantSerializer,
    ProductSerializer,
    TransactionSerializer,
)

from ..exceptions import InactiveProductError, InsufficientStockError
from ..models import Merchant, Product, Transaction
from ..pagination import CustomPagination
from ..services import StockManager


class MerchantAPIView(APIView):
    """
    API pour la gestion des commerçants
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "brand_name"]

    def get(self, request):
        queryset = Merchant.objects.filter(is_active=True)

        # Application des filtres
        queryset = DjangoFilterBackend().filter_queryset(request, queryset, self)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = MerchantSerializer(
            page if page is not None else queryset, many=True
        )

        return (
            paginator.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data)
        )

    def post(self, request):
        serializer = MerchantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MerchantDetailAPIView(APIView):
    """Détails d'un commerçant spécifique"""

    def get(self, request, pk):
        merchant = get_object_or_404(Merchant.objects.select_related("user"), pk=pk)
        serializer = MerchantDetailSerializer(merchant)
        return Response(serializer.data)

    def patch(self, request, pk):
        merchant = get_object_or_404(Merchant, pk=pk)
        serializer = MerchantDetailSerializer(
            merchant, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductAPIView(APIView):
    """Gestion des produits avec pagination custom"""

    pagination_class = CustomPagination

    def get(self, request, merchant_pk):
        queryset = Product.objects.filter(
            merchant_id=merchant_pk, is_active=True
        ).select_related("merchant")

        # Filtrage par catégorie
        if category := request.query_params.get("category"):
            queryset = queryset.filter(category=category)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(
            page if page is not None else queryset,
            many=True,
            context={"request": request},
        )

        return (
            paginator.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data)
        )

    def post(self, request, merchant_pk):
        merchant = get_object_or_404(Merchant, pk=merchant_pk)
        serializer = ProductSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(merchant=merchant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductStockAPIView(APIView):
    """Gestion des stocks"""

    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        try:
            quantity = int(request.data.get("quantity", 0))
            product.update_stock(quantity)
            return Response(
                {
                    "status": "success",
                    "data": {
                        "product_id": product.id,
                        "product_name": product.name,
                        "new_stock": product.stock,
                    },
                }
            )
        except (ValueError, InsufficientStockError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    """Gestion des transactions avec votre pagination"""

    pagination_class = CustomPagination

    def get(self, request, product_pk=None):
        queryset = Transaction.objects.select_related("product", "customer")
        if product_pk:
            queryset = queryset.filter(product_id=product_pk)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TransactionSerializer(
            page if page is not None else queryset, many=True
        )

        return (
            paginator.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data)
        )

    def post(self, request, product_pk):
        try:
            transaction = StockManager.process_sale(
                product_id=product_pk,
                quantity=request.data.get("quantity", 1),
                customer=request.user,
            )
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (InactiveProductError, InsufficientStockError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
