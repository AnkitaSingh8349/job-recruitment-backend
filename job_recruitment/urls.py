from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Job Recruitment API",
        default_version="v1",
        description="API documentation for Job Recruitment project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def home(request):
    return HttpResponse("""
        <h2>✅ Job Recruitment Backend is Live</h2>
        <p><a href="/docs/">Swagger Docs</a></p>
        <p><a href="/redoc/">ReDoc</a></p>
    """)


urlpatterns = [
    # Home
    path("", home),

    # Admin
    path("admin/", admin.site.urls),

    # ================ API ================
    # Accounts (auth)
    path("api/accounts/", include("accounts.urls")),

    # ✅ ADD THIS LINE (EMPLOYER REGISTER URL)
    path("api/employer/", include("employer.urls")),

    # IMPORTANT: applications.urls SHOULD come before jobs.urls
    path("api/", include("applications.urls")),
    path("api/", include("jobs.urls")),
    path("api/user/dashboard/", include("userdashboard.urls")),

    # Optional search
    path("api/", include("ajx_search.urls")),

    # ================ Docs ================
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
