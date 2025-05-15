DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "galerie",
        "USER": "kbf",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
        "OPTIONS": {
            "client_encoding": "UTF8",
            "connect_timeout": 5,
        },
        "CONN_MAX_AGE": 60 * 10,
    }
}
