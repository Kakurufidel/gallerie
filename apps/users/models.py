from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .constants import ROLE_CHOICES, ROLE_PERMISSIONS


class UserManager(models.Manager):
    """Custom manager for user creation methods"""

    def create_commercant(self, email, password, **extra_fields):
        """Helper method to create merchant users"""
        extra_fields.setdefault("role", "COMMERCE")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Extended User model with role-based system
    Contains all business logic related to users
    """

    # Extended fields
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Custom role field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CLIENT")

    # Status fields
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        permissions = [
            ("can_manage_commercants", "Can manage merchants"),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    # ----- Business Logic Methods -----

    @property
    def is_commercant(self):
        """Check if user has merchant role"""
        return self.role == "COMMERCE"

    def get_permissions(self):
        """Get permissions based on user role"""
        return ROLE_PERMISSIONS.get(self.role, [])

    def clean(self):
        """Data validation before saving"""
        if self.role == "COMMERCE" and not self.phone:
            raise ValidationError("Merchants must provide a phone number")

    def activate_commercant_account(self):
        """Special activation workflow for merchants"""
        if self.is_commercant:
            self.is_verified = True
            self.save(update_fields=["is_verified"])

    # Class methods
    @classmethod
    def get_commercants(cls):
        """Get all merchant users"""
        return cls.objects.filter(role="COMMERCE")
