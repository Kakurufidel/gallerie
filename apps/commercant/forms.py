from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Merchant, Product
from .product_constants import PRODUCT_CATEGORIES, VAT_RATES


class MerchantProfileForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ["brand_name", "description", "opening_hours", "shop_photo"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "opening_hours": forms.TextInput(
                attrs={"placeholder": '{"lundi": "9h-18h", "mardi": "9h-18h"}'}
            ),
        }
        labels = {
            "brand_name": _("Nom de la marque"),
            "shop_photo": _("Photo du commerce"),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "net_price",
            "vat_rate",
            "stock",
            "stock_alert_threshold",
            "photo",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "category": forms.Select(choices=PRODUCT_CATEGORIES),
            "vat_rate": forms.Select(
                choices=[
                    (rate, f"{name} ({rate*100}%)") for name, rate in VAT_RATES.items()
                ]
            ),
        }
        help_texts = {"stock_alert_threshold": _("Seuil pour les alertes de stock bas")}
