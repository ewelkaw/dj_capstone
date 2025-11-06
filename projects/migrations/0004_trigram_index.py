from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    dependencies = [("projects", "0003_task_task_proj_status_due_idx_and_more")]
    operations = [TrigramExtension()]
