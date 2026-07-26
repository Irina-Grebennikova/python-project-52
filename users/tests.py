from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    fixtures = ['users.json']

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
        response = self.client.get(reverse('users'))
        users = response.context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 2)

        self.assertTrue(User.objects.filter(username='user1').exists())
        self.assertTrue(User.objects.filter(username='user2').exists())

    def test_update_user(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'username': 'newname',
                'new_password1': 'newpassword',
                'new_password2': 'newpassword',
            },
        )

        self.assertEqual(response.status_code, 302)

        user.refresh_from_db()

        self.assertEqual(user.username, 'newname')

    def test_user_cannot_update_another_user(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')

        self.client.force_login(user2)
        self.client.post(reverse('user_update', kwargs={'pk': user1.pk}), {'username': 'new_name'})

        user1.refresh_from_db()

        self.assertEqual(user1.username, 'user1')

    def test_delete_user(self):
        user = User.objects.get(username='user1')
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=user.id).exists())
