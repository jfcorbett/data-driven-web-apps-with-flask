import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    return {}


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    # Show the form
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    # Process the submitted form
    r = flask.request

    name = r.form.get('name', '')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        # Show error message, but re-insert any existing name, email, pwd
        # in the form so the user doesn't lose what they did type in
        return {
            'error': "Some required fields are missing.",
            'name': name,
            'email': email,
            'password': password,
        }

    # TODO: create user in DB
    user = user_service.create_user(name, email, password)
    if not user:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': 'Could not create user. A user with that email already exists.'
        }
    # TODO: log in browser as a session
    return flask.redirect('/account')


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    return {}


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    return {}
