"""Homebrewed RequestBin"""
import flask


bp = flask.Blueprint('bin', __name__, url_prefix='/bin')


def is_nick():
    config = flask.current_app.config

    if not flask.session.get('logged_in', False):
        return False
    return flask.session['email'] == config['NICK_EMAIL']
        


@bp.route('/')
def home():
    if not is_nick():
        flask.abort(404)

    return 'You are nick'
