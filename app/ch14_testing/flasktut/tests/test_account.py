from flask import Response

from pypi_org.data.users import User
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from tests.client_for_tests import flask_app, client
import unittest.mock


def test_vm_register_validation_when_valid():
    # Arrange, Act, Assert

    # Arrange
    form_data = {
        'name': 'Alexander Bonaparte Cust',
        'email': 'abc@example.com',
        'password': 'a'*5,
    }
    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    # Mock this target function within the scope of this context manager
    with unittest.mock.patch(target=target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is None


def test_vm_register_validation_for_existing_user():

    # Arrange
    form_data = {
        'name': 'JF',
        'email': 'bac@abc.com',
        'password': 'a'*5,
    }
    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    target = 'pypi_org.services.user_service.find_user_by_email'
    # Mock this target function within the scope of this context manager
    test_user = User(email=form_data.get('email'))
    with unittest.mock.patch(target=target, return_value=test_user):

        # Act
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'exist' in vm.error


def test_v_register_new_user():

    # Arrange
    from pypi_org.views.account_views import register_post
    form_data = {
        'name': 'JF',
        'email': 'bac@abc.com',
        'password': 'a'*5,
    }

    # Mock all the services that talk to the DB
    find_user_by_email_mock = unittest.mock.patch(
        target='pypi_org.services.user_service.find_user_by_email', return_value=None)
    create_user_mock = unittest.mock.patch(target='pypi_org.services.user_service.create_user',
                                           return_value=User())
    request = flask_app.test_request_context(path='/account/register', data=form_data)
    with find_user_by_email_mock, create_user_mock, request:
        # Act
        resp: Response = register_post()

    # Assert
    assert resp.location == '/account'


def test_integ_account_home_no_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    with unittest.mock.patch(target, return_value=None):
        resp: Response = client.get('/account')

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/account/login'


def test_integ_account_home_with_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    test_user = User(name='Alex', email='abc@example.com')
    with unittest.mock.patch(target, return_value=test_user):
        resp: Response = client.get('/account')

    assert resp.status_code == 200
    assert b'Alex' in resp.data
