from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .roles import ROLE_CHOICES, ROLE_PERMISSIONS


class User(AbstractUser, PermissionsMixin):
    """
    Custom User model with role-based system and admin-compatible fields.
    """

    # Champs de base étendus
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=True,
        null=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    phone = models.CharField(_("phone number"), max_length=20, blank=True, null=True)

    birth_date = models.DateField(_("birth date"), null=True, blank=True)

    role = models.CharField(
        _("role"), max_length=20, choices=ROLE_CHOICES, default="CLIENT"
    )

    is_verified = models.BooleanField(_("verified status"), default=False)

    last_activity = models.DateTimeField(_("last activity"), auto_now=True)

    # Champs requis pour le superuser
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        app_label = "users"
        db_table = "users"
        permissions = [
            ("can_manage_merchants", _("Can manage merchants")),
        ]
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_merchant(self):
        """Check if user has merchant role"""
        return self.role == "MERCHANT"

    @property
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == "ADMIN" or self.is_superuser

    def get_permissions(self):
        """Get permissions based on user role"""
        perms = list(ROLE_PERMISSIONS.get(self.role, []))
        if self.is_superuser:
            perms.append("admin")
        return perms

    def clean(self):
        """Data validation before saving"""
        super().clean()

        if self.role == "MERCHANT" and not self.phone:
            raise ValidationError(
                _("Merchants must provide a phone number"), code="invalid_merchant"
            )

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def activate_merchant_account(self):
        """Special activation workflow for merchants"""
        if self.is_merchant:
            self.is_verified = True
            self.save(update_fields=["is_verified"])

    @classmethod
    def get_merchants(cls):
        """Get all merchant users"""
        return cls.objects.filter(role="MERCHANT")
