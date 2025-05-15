from django.core.validators import MinValueValidator, RegexValidator
from django.db import models, transaction
from django.utils import timezone

from apps.users.models import User

from .exceptions import InsufficientStockError
from .product_constants import PRODUCT_CATEGORIES, VAT_RATES


class Merchant(models.Model):
    """Core merchant model with complete business management"""

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "MERCHANT"},
        related_name="merchant_profile",
    )
    brand_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    opening_hours = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    # Business logic methods
    def add_product(self, name, price, category="FOOD", **kwargs):
        """Creates a new product with automatic validation"""
        if not self.is_active:
            raise ValueError("Inactive merchant - cannot add products")

        return Product.objects.create(
            merchant=self, name=name, price=price, category=category, **kwargs
        )

    def deactivate(self):
        """Deactivates merchant and related products"""
        self.is_active = False
        self.save(update_fields=["is_active"])
        self.products.update(is_active=False)

    # Computed properties
    @property
    def available_products(self):
        return self.products.filter(stock__gt=0, is_active=True)

    @property
    def revenue(self):
        return sum(t.amount for t in self.transactions.all())

    # Django standard methods
    class Meta:

        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["brand_name"]),
        ]


class Product(models.Model):
    """Complete product model with advanced stock management"""

    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20, choices=PRODUCT_CATEGORIES, default="FOOD"
    )
    net_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    vat_rate = models.DecimalField(
        max_digits=4, decimal_places=3, default=VAT_RATES["STANDARD"]
    )
    stock = models.PositiveIntegerField(default=0)
    stock_alert_threshold = models.PositiveIntegerField(default=5)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Business methods
    @property
    def gross_price(self):
        return round(self.net_price * (1 + self.vat_rate), 2)

    def update_stock(self, quantity):
        """Updates stock transactionally"""
        with transaction.atomic():
            if quantity < 0 and abs(quantity) > self.stock:
                raise InsufficientStockError(f"Insufficient stock for {self.name}")

            self.stock = models.F("stock") + quantity
            self.save(update_fields=["stock"])

            if self.stock < self.stock_alert_threshold:
                self.send_stock_alert()

    def send_stock_alert(self):
        """Notifies merchant about low stock"""
        # To be implemented with Celery or external service
        pass

    # Django methods
    def clean(self):
        """Data validation"""
        if self.net_price <= 0:
            raise ValidationError("Price must be positive")

    def save(self, *args, **kwargs):
        """Pre-save logic"""
        if not self.pk and self.stock < 0:
            raise ValidationError("Initial stock cannot be negative")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.merchant.brand_name})"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(net_price__gt=0), name="positive_net_price"
            ),
            models.CheckConstraint(
                check=models.Q(stock__gte=0), name="non_negative_stock"
            ),
        ]


class Transaction(models.Model):
    """Model for sales tracking"""

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="transactions"
    )
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "CUSTOMER"},
    )

    def save(self, *args, **kwargs):
        """Automatic amount calculation"""
        if not self.amount:
            self.amount = self.product.gross_price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["transaction_date"]),
        ]
