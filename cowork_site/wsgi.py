from .app import create_app
from . import config
from werkzeug.contrib.fixers import ProxyFix

app = create_app(config=config.Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)
