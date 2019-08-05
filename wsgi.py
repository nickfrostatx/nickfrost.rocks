from app import create_app

_app = None

def wsgi(environ, start_response):
    global _app
    if _app is None:
        _app = create_app()
    return _app(environ, start_response)
