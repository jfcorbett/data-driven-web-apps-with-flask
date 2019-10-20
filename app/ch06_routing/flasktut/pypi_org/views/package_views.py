import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import package_service

blueprint = flask.Blueprint('packages', __name__, template_folder='templates')


@blueprint.route('/project/<package_name>')
# @response(template_file='packages/details.html')
def package_details(package_name: str):
    return f"Package details for {package_name}"
    # return flask.render_template('home/index.html', packages=test_packages)

@blueprint.route('/<int:rank>')
# @response(template_file='packages/details.html')
def popular(rank: int):
    return f"Details for package ranking {rank} in popularity"
    # return flask.render_template('home/index.html', packages=test_packages)
