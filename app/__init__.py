from flask import Flask
from app.models import db
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        # Import routes inside to avoid circular imports
        from app.routes.main import main_bp
        from app.routes.ideas import ideas_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(ideas_bp)

        db.create_all()

    return app
