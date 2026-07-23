from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'testuser',
                'password1': 'password123',
                'password2': 'password123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_get_user_list(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        user2 = User.objects.create_user(username='user2', password='12345')
        response = self.client.get(reverse('users'))
        users = response.context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)

    def test_update_user(self):
        user = User.objects.create_user(username='oldname', password='12345')

        self.client.login(username='oldname', password='12345')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}), {'username': 'newname'}
        )

        self.assertEqual(response.status_code, 302)

        user.refresh_from_db()

        self.assertEqual(user.username, 'newname')

    def test_user_cannot_update_another_user(self):
        user1 = User.objects.create_user(username='user1', password='12345')
        User.objects.create_user(username='user2', password='12345')

        self.client.login(username='user2', password='12345')

        self.client.post(
            reverse('user_update', kwargs={'pk': user1.id}), {'username': 'hacked_name'}
        )

        user1.refresh_from_db()

        self.assertNotEqual(user1.username, 'hacked_name')

    def test_delete_user(self):
        user = User.objects.create_user(username='remove', password='123456')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=user.id).exists())
