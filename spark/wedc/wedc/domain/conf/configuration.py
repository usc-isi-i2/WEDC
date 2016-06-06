import os
import sys

from decouple import RepositoryEnv, Config

# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)

from wedc.domain.conf.storage import __root_dir__

settings_path_ = os.path.join(__root_dir__, 'settings.py')


def load_config(path=settings_path_):
    config = Config(RepositoryEnv(path))
    # config('TEST', default=25, cast=int)
    return config

    