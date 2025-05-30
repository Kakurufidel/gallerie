from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

api_patterns = [
    path("api/auth/", include("rest_framework.urls")),
    path("api/merchants/", include("apps.commercant.api.urls")),
    path("api/users/", include("apps.users.api.urls")),
]

urlpatterns += api_patterns

frontend_patterns = i18n_patterns(
    path("", include("apps.commercant.urls")),
    path("users/", include("apps.users.urls")),
    prefix_default_language=False,
)

urlpatterns += frontend_patterns

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
