from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "ADMIN" or self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied(_("Accès réservé aux administrateurs"))


class IsMerchantMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "MERCHANT"

    def handle_no_permission(self):
        raise PermissionDenied(_("Accès réservé aux marchands"))


class IsMerchantOwnerMixin(IsMerchantMixin):
    def test_func(self):
        if not super().test_func():
            return False
        obj = self.get_object()
        return obj.merchant.user == self.request.user
