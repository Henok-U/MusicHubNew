from .settings import Common


class Development(Common):
    DEBUG = True
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = 'django-insecure-o%=+4+n$6ip&msx6h+y@kuv295j#clj*-q!@^!x%eamf%d^8b^'