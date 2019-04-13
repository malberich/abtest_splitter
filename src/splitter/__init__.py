"""General features for the app."""
import os
from flask import Flask


def create_app():
    """Initialize all the routes and models."""
    from . import experiments
    from . import splits
    app = Flask(__name__)
    app.config.from_pyfile(
        "{}/config.py".format(os.getcwd())
    )

    experiments.init_app(app)
    splits.init_app(app)
    return app
