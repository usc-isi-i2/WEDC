import os
import sys

from decouple import RepositoryEnv, Config

# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)

settings_path_ = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.env')

def load_config(path=settings_path_):
    config = Config(RepositoryEnv(path))
    # config('TEST', default=25, cast=int)
    return config

    