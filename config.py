import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'english-learning-dev-key-78439284729184')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'instance', 'english_learning.db'))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max for backups
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
