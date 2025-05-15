from django.db import transaction

from .exceptions import InactiveProductError, InsufficientStockError
from .models import Product, Transaction


class StockManager:
    """Service for advanced stock management"""

    @classmethod
    def process_sale(cls, product_id, quantity, customer=None):
        """Processes a sale transactionally"""
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product_id)

            if not product.is_active:
                raise InactiveProductError("Product not available")

            product.update_stock(-quantity)
            transaction = Transaction.objects.create(
                product=product, quantity=quantity, customer=customer
            )

            return transaction


class MerchantReporting:
    """Service for business analytics"""

    @staticmethod
    def calculate_revenue(merchant_id, start_date, end_date):
        """Calculates revenue for a given period"""
        from django.db.models import Sum

        return (
            Transaction.objects.filter(
                product__merchant_id=merchant_id,
                transaction_date__range=(start_date, end_date),
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
