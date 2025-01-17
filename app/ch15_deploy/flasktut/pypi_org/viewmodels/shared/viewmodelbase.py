"""
Base class for all view models
This base class will be used for all templates
Each individual HTML template will need a view model that inherits from this base class
"""
from typing import Optional

import flask
from flask import Request

from pypi_org.infrastructure import request_dict, cookie_auth


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')

        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)

    def to_dict(self):
        return self.__dict__
