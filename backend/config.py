import os
import socket


def redis_is_available(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tma-jwt-super-secret-key-9988')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tma-jwt-extended-secret-key-1122')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400 * 30  # 30 days
    
    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, 'database')
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'database.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis-backed cache and Celery
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_AVAILABLE = redis_is_available(REDIS_HOST, REDIS_PORT)

    if REDIS_AVAILABLE:
        CACHE_TYPE = 'RedisCache'
        CACHE_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
        CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
        CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    else:
        CACHE_TYPE = 'SimpleCache'
        CACHE_DEFAULT_TIMEOUT = 300
        CELERY_BROKER_URL = 'memory://'
        CELERY_RESULT_BACKEND = 'cache+memory://'
