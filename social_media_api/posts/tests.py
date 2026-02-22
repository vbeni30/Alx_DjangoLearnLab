from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from notifications.models import Notification
from .models import Post, Like

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


class LikeUnlikeTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='pass12345')
        self.liker = User.objects.create_user(username='liker', password='pass12345')
        self.post = Post.objects.create(author=self.author, title='Post', content='Body')
        self.client.force_authenticate(user=self.liker)

    def test_like_post_creates_like_and_notification(self):
        url = reverse('like-post', kwargs={'pk': self.post.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.liker).exists())
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.author,
                actor=self.liker,
                verb='liked your post',
            ).exists()
        )

    def test_like_post_cannot_duplicate_like(self):
        Like.objects.create(post=self.post, user=self.liker)
        url = reverse('like-post', kwargs={'pk': self.post.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.filter(post=self.post, user=self.liker).count(), 1)

    def test_unlike_post_removes_like(self):
        Like.objects.create(post=self.post, user=self.liker)
        url = reverse('unlike-post', kwargs={'pk': self.post.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.liker).exists())

    def test_comment_creates_notification_for_post_author(self):
        commenter = User.objects.create_user(username='commenter', password='pass12345')
        self.client.force_authenticate(user=commenter)

        url = reverse('comment-list')
        response = self.client.post(
            url,
            data={'post': self.post.pk, 'content': 'Nice post'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.author,
                actor=commenter,
                verb='commented on your post',
            ).exists()
        )
