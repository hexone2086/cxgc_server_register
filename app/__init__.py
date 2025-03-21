from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_httpauth import HTTPBasicAuth

db = SQLAlchemy()
mail = Mail()

auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 添加 Basic Auth 验证
    @auth.verify_password
    def verify_password(username, password):
        return username == app.config['ADMIN_USERNAME'] and \
               password == app.config['ADMIN_PASSWORD']
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Import and register blueprints
    from .routes import bp as routes_bp
    from .api import bp as api_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)