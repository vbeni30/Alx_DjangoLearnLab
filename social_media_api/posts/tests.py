from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


class FeedTests(APITestCase):
    def setUp(self):
        self.viewer = User.objects.create_user(username='viewer', password='pass12345')
        self.followed = User.objects.create_user(username='followed', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')

        self.viewer.following.add(self.followed)

        self.followed_post_old = Post.objects.create(
            author=self.followed,
            title='Older followed post',
            content='Old content',
        )
        self.followed_post_new = Post.objects.create(
            author=self.followed,
            title='Newer followed post',
            content='New content',
        )
        self.other_post = Post.objects.create(
            author=self.other,
            title='Other post',
            content='Other content',
        )

        self.client.force_authenticate(user=self.viewer)

    def test_feed_returns_only_followed_users_posts(self):
        url = reverse('feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']

        returned_ids = [item['id'] for item in results]
        self.assertIn(self.followed_post_old.id, returned_ids)
        self.assertIn(self.followed_post_new.id, returned_ids)
        self.assertNotIn(self.other_post.id, returned_ids)

    def test_feed_is_ordered_newest_first(self):
        url = reverse('feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']

        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0]['id'], self.followed_post_new.id)

    def test_feed_requires_authentication(self):
        self.client.force_authenticate(user=None)

        url = reverse('feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
