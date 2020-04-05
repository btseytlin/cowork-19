from flask_caching import Cache
from cowork_site import config

cache = Cache(config={'CACHE_TYPE': config.Configuration.CACHE_TYPE,
                          'CACHE_DEFAULT_TIMEOUT':config.Configuration.CACHE_DEFAULT_TIMEOUT,
                          'CACHE_REDIS_HOST': config.Configuration.CACHE_HOST,
                          'CACHE_REDIS_PORT': config.Configuration.CACHE_PORT,
                          'CACHE_REDIS_DB': config.Configuration.CACHE_REDIS_DB})