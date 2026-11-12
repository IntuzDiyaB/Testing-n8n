"""
Application Configuration Management

Demonstrates best practices for managing environment-specific configurations
and sensitive data using environment variables.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class with common settings."""

    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = False

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION = timedelta(hours=24)

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'tasks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    # Rate limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_DEFAULT = '100/hour'


class DevelopmentConfig(Config):
    """Development environment configuration."""

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration."""

    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    # In production, these MUST be set via environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET = os.getenv('JWT_SECRET')

    if not SECRET_KEY or not JWT_SECRET:
        raise ValueError(
            'SECRET_KEY and JWT_SECRET must be set in production environment'
        )


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    DATABASE_URL = ':memory:'  # Use in-memory database for tests
    JWT_EXPIRATION = timedelta(minutes=5)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration object based on environment.

    Args:
        env (str, optional): Environment name. Defaults to FLASK_ENV.

    Returns:
        Config: Configuration class for the environment.

    Example:
        >>> cfg = get_config('production')
        >>> app.config.from_object(cfg)
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    return config.get(env, config['default'])
