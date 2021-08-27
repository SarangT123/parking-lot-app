from flask import Flask, Blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hjhgihjiuhgbjnksgdfvmaljgkdnni.kE NC,VJGNJMC"

    # Importing the view and auth .py's
    from .views import views
    from .owners import owners

    # Registering those blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(owners, url_prefix='/')
    return app
