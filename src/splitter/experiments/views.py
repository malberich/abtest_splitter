"""Route configuration for the experiments endpoint."""
from flask import current_app as app
from flask import Blueprint, abort, jsonify
from jinja2 import TemplateNotFound

experiments = Blueprint(
    'experiments',
    __name__,
    template_folder='templates'
)


@experiments.route('/experiments/')
def index():
    """Show the index page."""
    try:
        return jsonify(app.config['EXPERIMENTS']['experiments'])
    except TemplateNotFound:
        abort(404)


@experiments.route('/experiments/<experiment_id>', methods=['GET'])
def show(experiment_id):
    """Show the index page."""
    try:
        return jsonify([
            experiment for experiment
            in app.config['EXPERIMENTS']['experiments']
            if experiment['key'] == experiment_id][0]
        )
    except TemplateNotFound:
        abort(404)
