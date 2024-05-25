from flask import Flask
from config import Config
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    swagger = Swagger(app)

    with app.app_context():
        from .api import predict
        from .main import routes

        app.register_blueprint(predict.bp)
        app.register_blueprint(routes.bp)

    return app
