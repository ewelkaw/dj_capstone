from django.db import models
from django.utils.text import slugify
from django.db.models import Q


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:80]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "To do"
        DOING = "doing", "In progress"
        DONE = "done", "Done"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=140)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.TODO
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "title"], name="uniq_task_per_project"
            ),
        ]
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if len(self.title) < 3:
            raise ValueError("Title must be at least 3 characters long.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project} · {self.title}"
