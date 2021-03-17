from flask import Flask
from config import ConfigProd, ConfigDev, ConfigTest

def create_app():
    app = Flask(__name__,  static_url_path='/', static_folder='../docs/build/html/')
    if app.config["ENV"] == "production":
        configObject = ConfigProd()
    elif app.config["TESTING"] == True:
        configObject = ConfigTest()
    else:
        configObject = ConfigDev()
    
    app.config.from_object(configObject)

    @app.route('/')
    @app.route('/<path:path>')
    def serve_sphinx_docs(path='index.html'):
        #return "hello"
        return app.send_static_file(path)

    from registrationapi.routers.api import api
    app.register_blueprint(api)

    return app