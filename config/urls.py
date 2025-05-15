from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    # URLs techniques
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

# URLs d'API (non traduites)
api_patterns = [
    path("api/auth/", include("rest_framework.urls")),
    path("api/merchants/", include("apps.commercant.api.urls")),
    path("api/users/", include("apps.users.api.urls")),
]

urlpatterns += api_patterns

# URLs frontend avec prise en charge de la traduction
frontend_patterns = i18n_patterns(
    # Vos URLs d'application (seront préfixées par la langue)
    path("", include("apps.commercant.urls")),  # URLs templates commercant
    path("users/", include("apps.users.urls")),  # URLs templates users
    # Ajoutez d'autres apps ici
    prefix_default_language=False,  # Permet URLs sans préfixe pour la langue par défaut
)

urlpatterns += frontend_patterns

# Gestion des médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs de debug (si nécessaire)
# if settings.DEBUG:
#     from django.urls import re_path
#     from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView)

#     urlpatterns += [
#         # Documentation API
#         path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#         path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
#         # Debug Toolbar
#         re_path(r"^__debug__/", include("debug_toolbar.urls")),
#     ]
