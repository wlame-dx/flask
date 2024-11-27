from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    
    # Blueprint'i kaydet
    app.register_blueprint(main)
    
    return app