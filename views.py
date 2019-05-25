import base64
import hashlib
import os
import urllib.parse

import flask
from werkzeug.security import safe_str_cmp

bp = flask.Blueprint('views', __name__)

def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


@bp.route('/')
def home():
    return flask.render_template('home.html')

@bp.route('/googleauth')
def redirect_to_googleauth():
    state = _b64(hashlib.sha256(os.urandom(1024)).digest())
    flask.session['state'] = state

    config = flask.current_app.config
    
    qs = urllib.parse.urlencode([
        ('client_id', config['GOOGLE_OAUTH_CLIENT_ID']),
        ('response_type', 'code'),
        ('scope', 'openid email profile'),
        ('redirect_uri', 'https://nickfrost.rocks/oauth'),
        ('state', state),
        ('nonce', ''),
    ])
    google_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + qs
    return flask.redirect(google_url)


@bp.route('/oauth')
def oauth_authorize():
    state = request.args['state']
    if not safe_str_cmp(state, request.session['state']):
        return '', 400
    return 'hmm', 500
