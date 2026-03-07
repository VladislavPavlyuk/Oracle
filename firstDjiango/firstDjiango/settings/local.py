from .base import BASE_DIR

print('!!!LOCAL SETTINGS GET STARTED!!!')

DEBUG = True

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}