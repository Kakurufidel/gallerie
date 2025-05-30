from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from apps.commercant.forms import MerchantProfileForm, ProductForm
from apps.commercant.models import Merchant, Product, Transaction
from apps.users.views.mixins import IsMerchantMixin, IsMerchantOwnerMixin


class MerchantDashboardView(IsMerchantMixin, TemplateView):
    """Tableau de bord du commerçant"""

    template_name = "merchant/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        merchant = self.request.user.merchant_profile
        context.update(
            {
                "active_products": merchant.products.filter(is_active=True).count(),
                "low_stock_products": merchant.products.filter(
                    stock__lt=models.F("stock_alert_threshold"), is_active=True
                ),
                "recent_transactions": Transaction.objects.filter(
                    product__merchant=merchant
                ).order_by("-transaction_date")[:5],
            }
        )
        return context


class MerchantProfileView(IsMerchantMixin, UpdateView):
    """Gestion du profil marchand"""

    model = Merchant
    form_class = MerchantProfileForm
    template_name = "merchant/profile.html"
    success_url = reverse_lazy("merchant_dashboard")

    def get_object(self):
        return self.request.user.merchant_profile


class ProductListView(IsMerchantMixin, ListView):
    """Liste des produits du marchand"""

    model = Product
    template_name = "merchant/products/list.html"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(
            merchant=self.request.user.merchant_profile
        ).order_by("-is_active", "name")


class ProductCreateView(IsMerchantMixin, CreateView):
    """Création d'un nouveau produit"""

    model = Product
    form_class = ProductForm
    template_name = "merchant/products/form.html"
    success_url = reverse_lazy("merchant_products")

    def form_valid(self, form):
        form.instance.merchant = self.request.user.merchant_profile
        return super().form_valid(form)


class ProductUpdateView(IsMerchantOwnerMixin, UpdateView):
    """Mise à jour d'un produit"""

    model = Product
    form_class = ProductForm
    template_name = "merchant/products/form.html"
    success_url = reverse_lazy("merchant_products")


class ProductDetailView(IsMerchantOwnerMixin, DetailView):
    """Détail d'un produit"""

    model = Product
    template_name = "merchant/products/detail.html"


class StockManagementView(IsMerchantOwnerMixin, UpdateView):
    """Gestion des stocks"""

    model = Product
    fields = ["stock", "stock_alert_threshold"]
    template_name = "merchant/products/stock.html"
    success_url = reverse_lazy("merchant_products")

    def form_valid(self, form):
        # Logique supplémentaire pour l'historique des stocks
        return super().form_valid(form)


class TransactionListView(IsMerchantMixin, ListView):
    """Historique des transactions"""

    model = Transaction
    template_name = "merchant/transactions/list.html"
    paginate_by = 15

    def get_queryset(self):
        return (
            Transaction.objects.filter(
                product__merchant=self.request.user.merchant_profile
            )
            .select_related("customer")
            .order_by("-transaction_date")
        )


# Vues publiques
class PublicMerchantListView(ListView):
    """Liste publique des commerçants"""

    model = Merchant
    template_name = "public/merchants/list.html"
    queryset = Merchant.objects.filter(is_active=True)
    paginate_by = 12


class PublicMerchantDetailView(DetailView):
    """Profil public d'un commerçant"""

    model = Merchant
    template_name = "public/merchants/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(
            merchant=self.object, is_active=True, stock__gt=0
        )
        return context


class PublicProductDetailView(DetailView):
    """Détail public d'un produit"""

    model = Product
    template_name = "public/products/detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True, merchant__is_active=True, stock__gt=0)
        )
