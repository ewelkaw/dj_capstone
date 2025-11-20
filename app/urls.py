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
from django.contrib.auth import views as auth_views
from accounts.views import signup
from projects.views import (
    project_detail,
    project_list,
    project_create,
    project_update,
    project_delete,
<<<<<<< HEAD
=======
    task_create,
    task_delete,
    task_detail,
    task_list,
    task_update,
>>>>>>> feature/add_task_flow
)


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
    path("signup/", view=signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path("", view=project_list, name="project_list"),
    path("project_detail/<int:pk>", view=project_detail, name="project_detail"),
    path("project_create/", view=project_create, name="project_create"),
    path("project_update/<int:pk>", view=project_update, name="project_update"),
    path("project_delete/<int:pk>", view=project_delete, name="project_delete"),
<<<<<<< HEAD
=======
    path("task_list/", view=task_list, name="task_list"),
    path("task_detail/<int:pk>", view=task_detail, name="task_detail"),
    path("task_create/", view=task_create, name="task_create"),
    path("task_update/<int:pk>", view=task_update, name="task_update"),
    path("task_delete/<int:pk>", view=task_delete, name="task_delete"),
>>>>>>> feature/add_task_flow
]
