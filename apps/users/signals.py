# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import User


# @receiver(post_save, sender=User)
# def handle_user_creation(sender, instance, created, **kwargs):
#     """
#     Post-save signal handler for User model
#     Contains business logic that should execute after user creation
#     """
#     if created:
#         if instance.is_commercant:
#             # Send verification email to merchants
#             instance.send_verification_email()

#             # Automatically create merchant profile
#             from apps.commercants.models import Commercant

#             Commercant.objects.create(user=instance)
