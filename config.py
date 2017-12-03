# config.py

import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json',
                          'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


CONFIGS = {
    'dev': DevelopmentConfig,
    'stage': StagingConfig,
    'prod': ProductionConfig,
    'test': TestingConfig,
}

