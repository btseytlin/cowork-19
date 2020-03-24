from cowork_site.app import create_app
from cowork_site import config
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app(config=config.Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)
