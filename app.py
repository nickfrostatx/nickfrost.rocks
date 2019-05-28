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

    if 'SENTRY_DSN' in app.config:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
