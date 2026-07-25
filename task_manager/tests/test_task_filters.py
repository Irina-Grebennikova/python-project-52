from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Task


class TaskFilterTest(TestCase):
    fixtures = [
        'tasks.json',
        'statuses.json',
        'users.json',
        'labels.json',
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='user1')
        self.client.force_login(self.user)

    def test_tasks_without_filters(self):
        response = self.client.get(reverse('tasks'))

        tasks = response.context['object_list']

        self.assertEqual(
            tasks.count(),
            Task.objects.count(),
        )

    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks'),
            {
                'status': 2,
            },
        )

        tasks = response.context['object_list']

        for task in tasks:
            self.assertEqual(task.status_id, 2)

    def test_filter_by_assignee(self):
        response = self.client.get(
            reverse('tasks'),
            {
                'assignee': 2,
            },
        )

        tasks = response.context['object_list']

        for task in tasks:
            self.assertEqual(task.assignee_id, 2)

    def test_filter_by_label(self):
        response = self.client.get(
            reverse('tasks'),
            {
                'label': 1,
            },
        )

        tasks = response.context['object_list']

        for task in tasks:
            self.assertTrue(task.labels.filter(id=1).exists())

    def test_filter_by_author_own_tasks(self):
        response = self.client.get(
            reverse('tasks'),
            {
                'own_tasks': 'on',
            },
        )

        tasks = response.context['object_list']

        for task in tasks:
            self.assertEqual(task.author, self.user)

    def test_filter_by_status_and_assignee(self):
        response = self.client.get(
            reverse('tasks'),
            {
                'status': 2,
                'assignee': 2,
            },
        )

        tasks = response.context['object_list']

        for task in tasks:
            self.assertEqual(task.status_id, 2)
            self.assertEqual(task.assignee_id, 2)
