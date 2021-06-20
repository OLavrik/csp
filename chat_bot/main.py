import logging.config

import os
from flask import Flask, Blueprint
import settings as settings

from own.main_app import ns as blog_posts_namespace
from own.restplus import api

from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP



def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    flask_app.register_blueprint(blueprint)


if __name__ == "__main__":

    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host='0.0.0.0', port=settings.FLASK_SERVER_NAME, debug=settings.FLASK_DEBUG)
