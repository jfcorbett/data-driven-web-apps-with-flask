import flask

from infrastructure.view_modifiers import response

app = flask.Flask(__name__)


def get_latest_packages():
    return [
        {'name': 'flask', 'version': '1.2.3'},
        {'name': 'sqla', 'version': '666.66.666'},
        {'name': 'rainflo', 'version': '0.1', 'summary': 'Rainflow counting algorithm'},
    ]


@app.route('/')
@response(template_file='home/index.html')
def index():
    test_packages = get_latest_packages()
    return {'packages': test_packages}
    # instead of rendering template, we just return a dict, and @response will render
    # return flask.render_template('home/index.html', packages=test_packages)


@app.route('/about')
@response(template_file='home/about.html')
def about():
    return {}
    # return flask.render_template('home/about.html')


if __name__ == '__main__':
    app.run(debug=True)
