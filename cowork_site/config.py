from confi import BaseEnvironConfig, ConfigField, BooleanConfig, IntConfig


class Configuration(BaseEnvironConfig):
    DEBUG = BooleanConfig(default=True)
    TESTING = BooleanConfig(default=False)
    DB_ECHO = BooleanConfig(default=False)
    SECRET_KEY = ConfigField(default=__name__)
    SQLALCHEMY_URL = ConfigField(required=True)

    LOG_LEVEL = IntConfig(default=10)

    # Google auth
    GOOGLE_CLIENT_ID = ConfigField(required=True)
    GOOGLE_CLIENT_SECRET = ConfigField(required=True)
    OAUTHLIB_RELAX_TOKEN_SCOPE = BooleanConfig(default=True)
    OAUTHLIB_INSECURE_TRANSPORT = BooleanConfig(default=False)

    # Custom
    POSTINGS_PER_PAGE = IntConfig(default=20)
    ADMIN_EMAIL = ConfigField()