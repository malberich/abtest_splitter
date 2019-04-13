"""Splits blueprint initializer."""
from . import views


def init_app(app):
    """Register experiment blueprint."""
    app.register_blueprint(views.splits)
