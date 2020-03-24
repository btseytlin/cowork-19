from cowork_site.app import create_app
from cowork_site import config

if __name__ == "__main__":
    app = create_app(config=config.Configuration)
    app.run(host="0.0.0.0", port=8000)
