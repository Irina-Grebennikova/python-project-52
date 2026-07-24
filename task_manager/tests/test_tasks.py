from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Task


class TaskCRUDTest(TestCase):
    fixtures = ['tasks.json', 'statuses.json', 'users.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='user1')
        self.client.force_login(self.user)

    def test_create_task(self):
        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'Новая задача',
                'description': 'Описание задачи',
                'status': 1,
            },
        )

        new_task = Task.objects.get(name='Новая задача')

        self.assertTrue(new_task.author == self.user)
        self.assertRedirects(response, reverse('tasks'))

    def test_get_task_list(self):
        response = self.client.get(reverse('tasks'))
        tasks = response.context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tasks), 2)

        self.assertTrue(Task.objects.filter(name='Task 1').exists())
        self.assertTrue(Task.objects.filter(name='Task 2').exists())

    def test_get_task_detail(self):
        task = Task.objects.get(name='Task 1')

        response = self.client.get(reverse('task_detail', args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], task)
        self.assertContains(response, task.name)

    def test_update_task(self):
        task = Task.objects.get(name='Task 1')

        data = model_to_dict(task, fields=['description', 'status', 'assignee', 'author'])
        data['name'] = 'Новое имя'

        response = self.client.post(reverse('task_update', kwargs={'pk': task.pk}), data)

        task.refresh_from_db()

        self.assertEqual(task.name, 'Новое имя')
        self.assertRedirects(response, reverse('tasks'))

    def test_cannot_update_task_with_duplicate_name(self):
        task = Task.objects.get(name='Task 1')

        data = model_to_dict(task, fields=['description', 'status', 'assignee', 'author'])
        data['name'] = 'Task 2'

        response = self.client.post(reverse('task_update', kwargs={'pk': task.pk}), data)

        self.assertEqual(response.status_code, 200)

        task.refresh_from_db()

        self.assertEqual(task.name, 'Task 1')

    def test_user_cannot_see_tasks_without_login(self):
        self.client.logout()

        response = self.client.get(reverse('tasks'))

        self.assertRedirects(response, f'{reverse("login")}?next={reverse("tasks")}')

    def test_delete_tasks(self):
        task = Task.objects.get(name='Task 2')
        response = self.client.post(reverse('task_delete', kwargs={'pk': task.id}))

        self.assertFalse(Task.objects.filter(id=task.id).exists())
        self.assertRedirects(response, reverse('tasks'))

    def test_non_author_cannot_delete_task(self):
        task = Task.objects.get(name='Task 1')
        self.client.post(reverse('task_delete', kwargs={'pk': task.id}))

        self.assertTrue(Task.objects.filter(id=task.id).exists())
