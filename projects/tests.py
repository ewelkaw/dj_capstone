from django.test import TestCase
from .queries import (
    get_tasks_with_project,
    get_projects_with_tasks,
    search_tasks,
    top_projects_by_open_tasks,
    task_exists,
    lock_task_for_update,
)
from .models import Project, Task


class QueriesTestCase(TestCase):

    def test_get_tasks_with_project(self):
        # Create test data
        project = Project.objects.create(name="Test Project")
        Task.objects.create(title="Test Task 1", status="todo", project=project)
        Task.objects.create(title="Test Task 2", status="done", project=project)

        # Call the query function
        tasks = get_tasks_with_project([project.id])

        # Assert the expected results
        self.assertEqual(len(tasks), 2)
        expected = ["Test Task 1", "Test Task 2"]
        actual = [tasks[0].title, tasks[1].title]
        difference = set(expected) ^ set(actual)
        assert not difference

    def test_get_projects_with_tasks(self):
        # Create test data
        project1 = Project.objects.create(name="Test Project 1")
        project2 = Project.objects.create(name="Test Project 2")
        Task.objects.create(title="Test Task 1", status="todo", project=project1)
        Task.objects.create(title="Test Task 2", status="done", project=project2)

        # Call the query function
        projects = get_projects_with_tasks()

        # Assert the expected results
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0].name, "Test Project 1")
        self.assertEqual(projects[1].name, "Test Project 2")

    def test_search_tasks(self):
        # Create test data
        project = Project.objects.create(name="Test Project")
        Task.objects.create(title="Test Task 1", status="todo", project=project)
        Task.objects.create(title="Another Task", status="done", project=project)

        # Call the query function
        tasks = search_tasks("Test")

        # Assert the expected results
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task 1")

    def test_top_projects_by_open_tasks(self):
        # Create test data
        project1 = Project.objects.create(name="Test Project 1")
        project2 = Project.objects.create(name="Test Project 2")
        Task.objects.create(title="Test Task 1", status="todo", project=project1)
        Task.objects.create(title="Test Task 2", status="done", project=project2)

        # Call the query function
        projects = top_projects_by_open_tasks(1)

        # Assert the expected results
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "Test Project 1")

    def test_task_exists(self):
        # Create test data
        project = Project.objects.create(name="Test Project")
        task = Task.objects.create(title="Test Task", status="todo", project=project)

        # Call the query function
        exists = task_exists(task.id)

        # Assert the expected results
        self.assertTrue(exists)

    def test_lock_task_for_update(self):
        # Create test data
        project = Project.objects.create(name="Test Project")
        task = Task.objects.create(title="Test Task", status="todo", project=project)

        # Call the query function
        locked_task = lock_task_for_update(task.id)

        # Assert the expected results
        self.assertEqual(locked_task.id, task.id)
