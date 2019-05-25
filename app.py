import flask

import views


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(views.bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
