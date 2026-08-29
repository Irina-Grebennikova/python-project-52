from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_login(self.user)

        Status.objects.create(name='в работе')
        Status.objects.create(name='завершен')

    def test_create_status(self):
        response = self.client.post(
            reverse('status_create'),
            {
                'name': 'новый',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='новый').exists())

    def test_get_status_list(self):
        response = self.client.get(reverse('statuses'))
        statuses = response.context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(statuses), 2)

        self.assertTrue(Status.objects.filter(name='в работе').exists())
        self.assertTrue(Status.objects.filter(name='завершен').exists())

    def test_update_status(self):
        status = Status.objects.get(name='в работе')

        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}), {'name': 'на тестировании'}
        )

        self.assertEqual(response.status_code, 302)

        status.refresh_from_db()

        self.assertEqual(status.name, 'на тестировании')

    def test_cannot_update_status_with_duplicate_name(self):
        status = Status.objects.get(name='в работе')

        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}), {'name': 'завершен'}
        )

        self.assertEqual(response.status_code, 200)

        status.refresh_from_db()

        self.assertEqual(status.name, 'в работе')

    def test_user_cannot_see_statuses_without_login(self):
        self.client.logout()

        response = self.client.get(reverse('statuses'))

        self.assertRedirects(response, f'{reverse("login")}?next={reverse("statuses")}')

    def test_delete_status(self):
        status = Status.objects.get(name='в работе')
        response = self.client.post(reverse('status_delete', kwargs={'pk': status.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())
