from .models import Task, Project
from django.db.models import Count, Q
from django.utils.timezone import now
from django.db import transaction


def get_tasks_with_project(project_ids):
    return (
        Task.objects.select_related("project")
        .only("id", "title", "status", "project__id", "project__name")
        .filter(project_id__in=project_ids)
    )


def get_projects_with_tasks():
    return Project.objects.prefetch_related("tasks")


def search_tasks(terms):
    return Task.objects.filter(title__icontains=terms).only("id", "title")


def top_projects_by_open_tasks(n):
    return Project.objects.annotate(
        status_open=Count("tasks", filter=Q(tasks__status="todo"))
    ).order_by("-status_open")[:n]


def tasks_due_soon(days):
    return (
        Task.objects.filter(due_date__lte=now() + timedelta(days=days))
        .select_related("project")
        .values_list("id", "title", "due_date", "project__name")
    )


def task_exists(task_id):
    with transaction.atomic():
        return Task.objects.filter(id=task_id).exists()


transaction.atomic()


def lock_task_for_update(task_id):
    t = Task.objects.select_for_update(skip_locked=True).filter(id=task_id)
    return t.first()
