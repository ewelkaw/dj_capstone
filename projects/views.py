from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

import projects
from projects.forms import ProjectForm, TaskForm
from projects.models import Project, Task
from projects.permissions import require_owner_or_staff


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "project_list.html", {"projects": projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    print("Tasks XXXXX:", tasks)
    return render(request, "project_detail.html", {"project": project, "tasks": tasks})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return render(request, "project_detail.html", {"project": project})
        else:
            form = ProjectForm()
            return render(request, "project_create.html", {"form": form})
    form = ProjectForm()
    return render(request, "project_create.html", {"form": form})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm
    if request.method == "POST":
        form = form(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return render(request, "project_detail.html", {"project": project})
        else:
            # print("Form errors:", form.errors)
            return form.errors
    return render(request, "project_update.html", {"form": form(), "project": project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        require_owner_or_staff(request.user, project)
        project.delete()
        projects = Project.objects.filter(owner=request.user)
        return render(request, "project_list.html", {"projects": projects})
    return render(request, "project_delete.html", {"project": project})


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user, project=request.project)
    return render(request, "task_list.html", {"tasks": tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task_detail.html", {"task": task, "project": task.project})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return render(
                request, "task_detail.html", {"task": task, "project": task.project}
            )
        else:
            form = TaskForm()
            return render(request, "task_create.html", {"form": form})
    form = TaskForm()
    return render(request, "task_create.html", {"form": form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = TaskForm
    if request.method == "POST":
        form = form(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return render(
                request, "task_detail.html", {"task": task, "project": task.project}
            )
    return render(request, "task_update.html", {"form": form, "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        require_owner_or_staff(request.user, task)
        task.delete()
        tasks = Task.objects.filter(owner=request.user)
        return render(request, "task_list.html", {"tasks": tasks})
    return render(request, "task_delete.html", {"task": task})
