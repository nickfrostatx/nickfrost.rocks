import base64
import hashlib
import os
import urllib.parse

import flask
import jwt
import requests
from werkzeug.security import safe_str_cmp

bp = flask.Blueprint('views', __name__)

def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


@bp.route('/')
def home():
    if flask.session.get('logged_in', False):
        return flask.render_template('why.html')
    else:
        return flask.render_template('home.html')


@bp.route('/googleauth')
def redirect_to_googleauth():
    config = flask.current_app.config

    state = _b64(hashlib.sha256(os.urandom(1024)).digest())
    flask.session['state'] = state
    
    qs = urllib.parse.urlencode([
        ('client_id', config['GOOGLE_OAUTH_CLIENT_ID']),
        ('response_type', 'code'),
        ('scope', 'openid email profile'),
        ('redirect_uri', config['GOOGLE_OAUTH_REDIRECT_URI']),
        ('state', state),
    ])
    google_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + qs
    return flask.redirect(google_url)


@bp.route('/oauth')
def oauth_authorize():
    config = flask.current_app.config

    state = flask.request.args['state']
    if not safe_str_cmp(state, flask.session['state']):
        return 'Invalid state parameter', 400
    del flask.session['state']

    code = flask.request.args['code']
    rv = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'code': code,
            'client_id': config['GOOGLE_OAUTH_CLIENT_ID'],
            'client_secret': config['GOOGLE_OAUTH_CLIENT_SECRET'],
            'redirect_uri': config['GOOGLE_OAUTH_REDIRECT_URI'],
            'grant_type': 'authorization_code',
        },
    )
    if not rv.ok:
        raise Exception(rv.text)
    id_token = rv.json()['id_token']
    # Google just gave this to us over HTTPS. We don't need to bother with
    # verifying the signature.
    profile = jwt.decode(id_token, verify=False)

    flask.session.permanent = True
    flask.session['logged_in'] = True
    flask.session['name'] = profile['name']
    flask.session['email'] = profile['email']
    flask.session['picture'] = profile['picture']

    return flask.redirect(flask.url_for('.home'))
