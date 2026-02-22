from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from notifications.models import Notification

User = get_user_model()


class FollowUnfollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass12345')
        self.user2 = User.objects.create_user(username='bob', password='pass12345')
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse('follow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.user1.following.all())
        self.assertIn(self.user1, self.user2.followers.all())
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user2,
                actor=self.user1,
                verb='started following you',
            ).exists()
        )

    def test_unfollow_user(self):
        self.user1.following.add(self.user2)

        url = reverse('unfollow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user2, self.user1.following.all())

    def test_cannot_follow_self(self):
        url = reverse('follow-user', kwargs={'user_id': self.user1.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        url = reverse('follow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
