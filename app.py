import flask

import views


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('config')
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
    )
    app.register_blueprint(views.bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
