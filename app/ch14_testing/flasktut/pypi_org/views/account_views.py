import flask

from pypi_org.infrastructure import request_dict
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service
import pypi_org.infrastructure.cookie_auth as cookie_auth
from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')
    return vm.to_dict()


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    # Process the submitted form
    vm = RegisterViewModel()  # < all data validation is moved into viewmodel
    vm.validate()

    if vm.error:
        # round trip all user input and pass error message
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created.'
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    data = request_dict.create()  # Michael Kennedy's pattern

    email = data.email.lower().strip()
    password = data.password.strip()

    if not email or not password:
        # Show error message, but re-insert any existing name, email, pwd
        # in the form so the user doesn't lose what they did type in
        return {
            'error': "Some required fields are missing.",
            'email': email,
            'password': password,
        }

    #TODO Validate the user
    user = user_service.login_user(email, password)
    if not user:
        return {
            'email': email,
            'password': password,
            'error': 'The account does not exist or the password is wrong.'
        }

    # log in browser as a session
    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
