# Social Media API

## New Features: Likes and Notifications

This API now supports post likes and in-app notifications for social interactions.

## Models Added

### `posts.Like`
Tracks which users liked which posts.
- `post` (ForeignKey to `posts.Post`)
- `user` (ForeignKey to `accounts.User`)
- `created_at`
- Unique per `(post, user)`

### `notifications.Notification`
Tracks user-facing events.
- `recipient` (ForeignKey to `accounts.User`)
- `actor` (ForeignKey to `accounts.User`)
- `verb` (action text)
- `target` (`GenericForeignKey`)
- `timestamp`
- `is_read`

Notifications are generated for:
- New followers
- Likes on your posts
- Comments on your posts

## Endpoints

All endpoints are under `/api/` and require token auth unless noted.

### Follow/Unfollow
- `POST /api/follow/<user_id>/`
- `POST /api/unfollow/<user_id>/`

### Feed
- `GET /api/feed/`

### Likes
- `POST /api/posts/<pk>/like/`
- `POST /api/posts/<pk>/unlike/`

### Notifications
- `GET /api/notifications/`

Returns notifications for the authenticated user, ordered with unread first.

## Example Auth Header

`Authorization: Token <your_token>`

## Setup / Migrations

```bash
py manage.py makemigrations
py manage.py migrate
```

## Tests

```bash
py manage.py test
```

Covers:
- follow/unfollow behavior
- feed behavior
- like/unlike behavior
- notification generation (follow/like/comment)
- notifications list endpoint behavior

## Deployment (Production)

Production-ready deployment files are included:
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `build.sh`
- `render.yaml`
- `.env.example`

Detailed deployment instructions:
- `DEPLOYMENT.md`
