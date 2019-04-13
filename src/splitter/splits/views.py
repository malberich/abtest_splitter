"""Route configuration for the experiments endpoint."""
from flask import current_app as app
from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound

from ..common import audience_filter, get_split

splits = Blueprint(
    'splits',
    __name__,
    template_folder='templates'
)


@splits.route('/splits/')
def index():
    """Show the index page."""
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@splits.route(
    '/splits/<user_id>/',
    methods=['GET', 'POST'],
    defaults={'split_id': None}
)
@splits.route(
    '/splits/<user_id>/<split_id>/',
    methods=['GET', 'POST']
)
def show(user_id, split_id):
    """Get or set a given split for this user."""
    # print(app.config)
    user_splits = []
    try:
        if 'POST' in request.method:
            pass
        else:
            if split_id is None:
                for experiment in app.config['EXPERIMENTS']['experiments']:
                    # print(experiment)
                    user_audience = audience_filter(
                        "{}{}".format(
                            experiment['key'],
                            user_id
                        ),
                        experiment['audience']
                    )
                    user_assignment = {
                        'experiment_id': experiment['key'],
                    }
                    if user_audience is True:
                        assigned_group = get_split(
                            "{}{}".format(
                                user_id,
                                experiment['key']
                            ),
                            experiment['groups']
                        )
                        user_assignment['group'] = assigned_group
                        user_assignment['group_name'] = experiment['groups'][
                            assigned_group
                        ]
                    else:
                        user_assignment['group'] = app.config['EXPERIMENTS'][
                            'general'
                        ]['excluded_group']
                        user_assignment['group_name'] = {
                            'key': '(Excluded)',
                            'size': experiment['audience']
                        }
                    user_splits.append(user_assignment)

        return jsonify(user_splits)
    except TemplateNotFound:
        abort(404)


# @splits.route(
#     '/splits/',
#     methods=['PUT'],
#     defaults={'user_id': None, 'id': None}
# )
# @splits.route(
#     '/splits/<user_id>',
#     methods=['PUT'],
#     defaults={'id': None}
# )
# @splits.route(
#     '/splits/<user_id>/<id>',
#     methods=['PUT']
# )
# def update():
#     """Try to override a given user split."""
#     try:
#         return render_template('update.html')
#     except TemplateNotFound:
#         abort(404)


# @splits.route(
#     '/splits/',
#     methods=['DELETE'],
#     defaults={'user_id': None, 'id': None}
# )
# @splits.route(
#     '/splits/<user_id>',
#     methods=['DELETE'],
#     defaults={'id': None}
# )
# @splits.route(
#     '/splits/<user_id>/<id>',
#     methods=['DELETE']
# )
# def delete():
#     """Delete an existing experiment."""
#     try:
#         return render_template('delete.html')
#     except TemplateNotFound:
#         abort(404)
