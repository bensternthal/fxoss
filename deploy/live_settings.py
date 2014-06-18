from __future__ import unicode_literals

SECRET_KEY = "{{secret_key}}"
NEVERCACHE_KEY = "{{nevercache_key}}"

DEFAULT_FROM_EMAIL = "{{default_from_email}}"
EMAIL_HOST = "{{email_host}}"
SERVER_EMAIL = "{{server_email}}"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "{{proj_name}}",
        # Not used with sqlite3.
        "USER": "{{proj_name}}",
        # Not used with sqlite3.
        "PASSWORD": "{{db_pass}}",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "127.0.0.1",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

CACHE_MIDDLEWARE_SECONDS = 60

CACHE_MIDDLEWARE_KEY_PREFIX = "{{proj_name}}"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SALESFORCE = {{salesforce}}
