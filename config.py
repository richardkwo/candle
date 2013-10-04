#-*-coding:utf-8-*-

EMAIL_ACCOUNT = ''
EMAIL_PWD = ''
EMAIL_HOST = ''
EMAIL_PORT = ''

# use sentry to log exceptions? this is optional
SENTRY_DSN = ''

try:
    from local_config import *
except ImportError:
    pass

