# Deploying `social_media_api` to Production

This project is productionized for deployment with Gunicorn + PostgreSQL and can be deployed on Render (recommended here), Heroku-like platforms, or a VM with Nginx reverse proxy.

## 1. Production Settings Implemented

`social_media_api/settings.py` is environment-driven and includes:
- `DEBUG` from env (default `False`)
- `ALLOWED_HOSTS` from env
- `DATABASE_URL` support via `dj-database-url`
- Security hardening:
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `X_FRAME_OPTIONS = "DENY"`
  - `SECURE_SSL_REDIRECT = True` (unless `DEBUG=True`)
  - secure cookies + HSTS
- Static file handling with WhiteNoise:
  - `STATIC_ROOT = BASE_DIR / "staticfiles"`
  - `collectstatic` during build

## 2. Hosting Service Choice

Recommended: **Render**
- Managed Python runtime
- Managed PostgreSQL integration
- Easy environment variable management

## 3. Web Server / WSGI

Configured to run with **Gunicorn**:
- `Procfile`: `web: gunicorn social_media_api.wsgi --log-file -`
- `render.yaml` start command uses Gunicorn

If deploying to your own VPS, put **Nginx** in front of Gunicorn for reverse proxy and HTTPS.

## 4. Static Files and Database

- Static files:
  - `python manage.py collectstatic --no-input`
  - Served by WhiteNoise
- Database:
  - Production uses `DATABASE_URL` (PostgreSQL recommended)
  - Example in `.env.example`

## 5. Deployment Process (Render)

1. Push repository to GitHub.
2. Create a new Render Web Service from the repo.
3. Use `render.yaml` blueprint deploy, or manually configure:
   - Build command: `./build.sh`
   - Start command: `gunicorn social_media_api.wsgi --log-file -`
4. Set env vars:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=<your-render-domain>`
   - `CSRF_TRUSTED_ORIGINS=https://<your-render-domain>`
   - `DATABASE_URL` (from managed Postgres)
5. Deploy.

## 6. Monitoring and Maintenance

- Logs: use Render service logs (`stdout`/`stderr` from Gunicorn)
- Keep dependencies updated regularly
- Run test suite before each release:

```bash
py manage.py test
```

## 7. Final Verification Checklist

- `GET /api/posts/` responds in production
- Token auth works (`/api/login/`)
- Follow/feed/like/notification endpoints return expected responses
- Static files load without 404s
- HTTPS is enforced

## Deployment Artifacts Delivered

- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `.env.example`
- `build.sh`
- `render.yaml`

## Live URL

Set this after your first successful deployment:

- `https://<your-service-name>.onrender.com/`
