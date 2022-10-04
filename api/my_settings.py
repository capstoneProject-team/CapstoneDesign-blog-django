#my_setting.py
import environ
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# reading .env file
env = environ.Env.read_env(
    env_file = os.path.join(BASE_DIR, '.env')
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hed',
        'USER': 'root',
        'PASSWORD': 1234,
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

SECRET_KEY = env('JWT_SECRET_KEY')