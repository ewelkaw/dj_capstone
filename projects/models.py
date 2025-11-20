from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.db.models import Q, F
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import PermissionDenied


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="owned_%(class)ss",
        null=True,
        blank=True,
    )
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
    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="owned_%(class)ss",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "title"], name="uniq_task_per_project"
            ),
            models.CheckConstraint(
                check=Q(due_date__isnull=True) | Q(due_date__gte=F("created_at")),
                name="task_due_after_created",
            ),
        ]
        indexes = [
            models.Index(
                fields=["project", "status", "due_date"],
                name="task_proj_status_due_idx",
            ),
            GinIndex(
                name="task_title_trgm",
                fields=["title"],
                opclasses=["gin_trgm_ops"],
            ),
        ]
        ordering = ["-created_at"]

    def clean(self):
        if self.title and len(self.title) < 3:
            raise ValidationError(
                {"title": "Title must be at least 3 characters long."}
            )

    def save(self, *args, **kwargs):
        # runs clean() + field validators + unique checks
        # this will raise ValidationError, which Django forms know how to display
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project} · {self.title}"
