from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# --------------------
# Swagger configuration
# --------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Job Recruitment API",
        default_version="v1",
        description="API documentation for Job Recruitment project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# --------------------
# Home page (to avoid 404 on /)
# --------------------
def home(request):
    return HttpResponse("""
        <html>
            <head>
                <title>Job Recruitment Backend</title>
            </head>
            <body style="font-family: Arial; padding: 40px;">
                <h2>✅ Job Recruitment Backend is Live</h2>
                <p>
                    👉 <a href="/docs/">Open Swagger API Docs</a>
                </p>
                <p>
                    👉 <a href="/redoc/">Open ReDoc</a>
                </p>
            </body>
        </html>
    """)


# --------------------
# URL patterns
# --------------------
urlpatterns = [
    path("", home),  # 👈 ROOT URL (no more 404)

    path("admin/", admin.site.urls),

    # Apps
    path("api/accounts/", include("accounts.urls")),
    path("api/jobs/", include("jobs.urls")),

    # Swagger docs
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]


# --------------------
# Static files (Swagger CSS/JS fix)
# --------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
