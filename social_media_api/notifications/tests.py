from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Notification

User = get_user_model()


class NotificationListTests(APITestCase):
    def setUp(self):
        self.recipient = User.objects.create_user(username='recipient', password='pass12345')
        self.actor = User.objects.create_user(username='actor', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')

        Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            verb='liked your post',
            is_read=True,
        )
        Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            verb='commented on your post',
            is_read=False,
        )
        Notification.objects.create(
            recipient=self.other,
            actor=self.actor,
            verb='started following you',
            is_read=False,
        )

        self.client.force_authenticate(user=self.recipient)

    def test_notifications_endpoint_returns_only_current_user_notifications(self):
        url = reverse('notifications-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_unread_notifications_are_listed_first(self):
        url = reverse('notifications-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertFalse(results[0]['is_read'])
