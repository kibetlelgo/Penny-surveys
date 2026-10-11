# Deploying PennySurveys to Vercel

Vercel's serverless filesystem is not a persistent place to store SQLite data. Use a hosted PostgreSQL or MySQL database instead. Both are supported through `DATABASE_URL`.

For a temporary demo without a hosted database, leave `DATABASE_URL` unset. On Vercel the app uses SQLite under `/tmp` and runs migrations when the function starts. This may let registration and login work during a warm instance, but database contents can disappear at any time and are not shared reliably between instances. Do not use this mode for real users or important data.

1. Create a PostgreSQL or MySQL database and copy its connection URL. PostgreSQL URLs use the `postgres://` or `postgresql://` scheme; MySQL URLs use `mysql://`. Follow your provider's instructions for SSL and URL-encoding special characters in credentials.
2. In the Vercel project, add `DATABASE_URL` with that connection URL under **Settings > Environment Variables**. Add it to every environment where the app runs, then redeploy.
3. Set `SECRET_KEY` to a secure generated value, `DEBUG` to `False`, and `ALLOWED_HOSTS` to `penny-surveys.vercel.app` (plus any custom domains).
4. Run database migrations against that same database before serving registration requests:

```bash
python manage.py migrate
```

For PostgreSQL or MySQL, run the migration command from an environment with the Vercel `DATABASE_URL` configured, or as a one-off deployment step. Do not use `sqlite:///db.sqlite3` for Vercel; SQLite remains the local-development default outside the temporary demo mode above.
