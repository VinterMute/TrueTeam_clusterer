import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'powerful secret key'
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'a csrf secret key'
