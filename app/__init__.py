from flask import Config, Flask, g

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.api.routes import bp
    #from api.subscriptions.routes import subscription
    #from api.main.routes import blueprint
    #from api.parsers.routes import parser
    app.register_blueprint(bp)
    #app.register_blueprint(subscriptions)
    #app.register_blueprint(blueprint)

    return app