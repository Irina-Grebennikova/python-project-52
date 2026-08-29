from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_login(self.user)

        feature_label = Label.objects.create(name='feature')
        Label.objects.create(name='bug')
        status = Status.objects.create(name='в работе')
        task = Task.objects.create(name='Task 1', author=self.user, status=status)
        task.labels.add(feature_label)

    def test_create_label(self):
        response = self.client.post(
            reverse('label_create'),
            {
                'name': 'new',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='new').exists())

    def test_get_label_list(self):
        response = self.client.get(reverse('labels'))
        labels = response.context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(labels), 2)

        self.assertTrue(Label.objects.filter(name='feature').exists())
        self.assertTrue(Label.objects.filter(name='bug').exists())

    def test_update_label(self):
        label = Label.objects.get(name='feature')

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}), {'name': 'technical issue'}
        )

        self.assertEqual(response.status_code, 302)

        label.refresh_from_db()

        self.assertEqual(label.name, 'technical issue')

    def test_cannot_update_label_with_duplicate_name(self):
        label = Label.objects.get(name='feature')

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}), {'name': 'bug'}
        )

        self.assertEqual(response.status_code, 200)

        label.refresh_from_db()

        self.assertEqual(label.name, 'feature')

    def test_user_cannot_see_labels_without_login(self):
        self.client.logout()

        response = self.client.get(reverse('labels'))

        self.assertRedirects(response, f'{reverse("login")}?next={reverse("labels")}')

    def test_delete_label(self):
        label = Label.objects.get(name='bug')
        response = self.client.post(reverse('label_delete', kwargs={'pk': label.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label.id).exists())

    def test_cannot_delete_used_label(self):
        label = Label.objects.get(name='feature')
        response = self.client.post(reverse('label_delete', kwargs={'pk': label.id}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=label.id).exists())
