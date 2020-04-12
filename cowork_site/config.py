from confi import BaseEnvironConfig, ConfigField, BooleanConfig, IntConfig


class Configuration(BaseEnvironConfig):
    DEBUG = BooleanConfig(default=True)
    TESTING = BooleanConfig(default=False)
    DB_ECHO = BooleanConfig(default=False)
    SECRET_KEY = ConfigField(default=__name__)
    SQLALCHEMY_URL = ConfigField(required=True)

    LOG_LEVEL = IntConfig(default=20)

    # Google auth
    GOOGLE_CLIENT_ID = ConfigField(required=True)
    GOOGLE_CLIENT_SECRET = ConfigField(required=True)
    OAUTHLIB_RELAX_TOKEN_SCOPE = BooleanConfig(default=True)
    OAUTHLIB_INSECURE_TRANSPORT = BooleanConfig(default=False)

    # Sentry
    SENTRY_DSD = ConfigField()

    # Custom
    POSTINGS_PER_PAGE = IntConfig(default=20)
    ADMIN_EMAILS = ConfigField(processor=lambda text: [t.strip().lower() for t in text.split(',') if t.strip()])

    # Cache
    CACHE_TYPE = ConfigField(default='redis')
    CACHE_DEFAULT_TIMEOUT = IntConfig(default=9999)
    CACHE_HOST = ConfigField(default='redis')
    CACHE_PORT = IntConfig(default=6379)
    CACHE_REDIS_DB = IntConfig(default=0)
