from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager personnalisé pour la création d'utilisateurs"""

    def create_user(self, email, password=None, **extra_fields):
        """Crée un utilisateur standard"""
        if not email:
            raise ValueError("Email obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_commercant(self, email, password, siret, **extra_fields):
        """Crée un utilisateur commerçant avec son profil"""
        extra_fields.setdefault("role", "COMMERCE")
        user = self.create_user(email, password, **extra_fields)
        user.make_commercant(siret)  # Utilise la méthode du modèle
        return user
