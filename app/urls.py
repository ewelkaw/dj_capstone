"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.db import connection


def healthz(_):
    return JsonResponse({"ok": True})


def liveness(_request):
    return JsonResponse({"ok": True})


def readiness(_request):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        return JsonResponse({"ready": True})
    except Exception as e:
        return JsonResponse({"ready": False, "error": str(e)}, status=503)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz),
    path("liveness/", liveness),
    path("readiness/", readiness),
]
