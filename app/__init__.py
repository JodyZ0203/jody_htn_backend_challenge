from flask import Config, Flask, g


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.api.routes import bp

    app.register_blueprint(bp)

    return app
