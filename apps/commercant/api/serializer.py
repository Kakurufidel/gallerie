from rest_framework import serializers

from ..models import Merchant, Product, Transaction


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id", "brand_name", "description", "is_active"]
        read_only_fields = ["id"]


class MerchantDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Merchant
        fields = "__all__"

    def get_products(self, obj):
        return ProductSerializer(obj.products.filter(is_active=True), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    gross_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["merchant", "creation_date"]

    def get_gross_price(self, obj):
        return obj.gross_price


class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "amount",
            "transaction_date",
        ]
