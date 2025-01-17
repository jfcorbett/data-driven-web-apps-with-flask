# import os
# import sys
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, folder)
import flask

app = flask.Flask(__name__)


def main():
    register_blueprints()
    app.run(debug=True)


def register_blueprints():
    from pypi_org.views import home_views, package_views, cms_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(cms_views.blueprint)


if __name__ == '__main__':
    main()
