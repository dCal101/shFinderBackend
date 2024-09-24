from flask import Flask
from flask_cors import CORS
import os

from logging import FileHandler,WARNING

def create_app():
    app = Flask(__name__)
    #if os.environ.get('FLASK_ENV') == 'development':
    CORS(app)
    from api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    #from app.utils.gemini_middleware import gemini_middleware
    #app.register_blueprint(gemini_middleware)

    #file_handler = FileHandler('errorlog.txt')
    #file_handler.setLevel(WARNING)



    return app