from rest_framework import serializers

from ..models import Merchant, Product, Transaction


class MerchantSerializer(serializers.ModelSerializer):
    shop_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Merchant
        fields = ["id", "brand_name", "description", "is_active", "shop_photo_url"]
        read_only_fields = ["id", "shop_photo_url"]

    def get_shop_photo_url(self, obj):
        if obj.shop_photo:
            return obj.shop_photo.url
        return None


class MerchantDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    shop_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Merchant
        fields = "__all__"
        extra_kwargs = {"shop_photo": {"write_only": True}}

    def get_products(self, obj):
        return ProductSerializer(obj.products.filter(is_active=True), many=True).data

    def get_shop_photo_url(self, obj):
        if obj.shop_photo:
            return obj.shop_photo.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    gross_price = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["merchant", "creation_date", "photo_url"]
        extra_kwargs = {"photo": {"write_only": True}}

    def get_gross_price(self, obj):
        return obj.gross_price

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "product",
            "product_name",
            "product_photo_url",
            "quantity",
            "amount",
            "transaction_date",
        ]

    def get_product_photo_url(self, obj):
        if obj.product.photo:
            return obj.product.photo.url
        return None
