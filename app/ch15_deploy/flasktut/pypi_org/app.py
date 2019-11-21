# import os
# import sys
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, folder)
import os

import flask

import pypi_org.data.db_session as db_session

app = flask.Flask(__name__)


def main():
    configure()
    app.run(debug=True)


def configure():
    print("Configuring Flask app:")

    register_blueprints()
    print("Registered blueprints.")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'db', 'pypi.sqlite')
    db_session.global_init(db_file)


def register_blueprints():
    from pypi_org.views import home_views, package_views, cms_views, account_views, seo_view
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(cms_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(seo_view.blueprint)


if __name__ == '__main__':
    # Start the (dev) server
    main()
else:
    # Presumably uWSGI got uw here.
    # Don't start the server,
    # but still need to set it up for uWSGI.
    configure()
