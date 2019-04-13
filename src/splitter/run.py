"""Running component for the main app."""
from . import create_app
from .common import audience_filter, get_split

if __name__ == "__main__":
    app = create_app()
    application = app
    app.run(host='0.0.0.0')
