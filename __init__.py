from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'development-only-change-before-deploy'

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    return app
