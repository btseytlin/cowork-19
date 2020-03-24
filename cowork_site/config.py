from confi import BaseEnvironConfig, ConfigField, BooleanConfig, IntConfig


class Configuration(BaseEnvironConfig):
    DEBUG = BooleanConfig(default=True)
    TESTING = BooleanConfig(default=False)
    DB_ECHO = BooleanConfig(default=False)
    SECRET_KEY = ConfigField(default=__name__)
    SQLALCHEMY_URL = ConfigField(required=True)

    LOG_LEVEL = IntConfig(default=10)
