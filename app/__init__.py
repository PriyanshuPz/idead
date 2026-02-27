from datetime import datetime, timezone
import os

from flask import Flask
from app.models import db
from app.utils.schema import ensure_schema_compatibility
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)
    app.config["BUILD_TIMESTAMP"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    # Ensure the default SQLite path is writable when running in containers.
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    @app.context_processor
    def inject_build_metadata():
        return {"last_built": app.config.get("BUILD_TIMESTAMP")}

    with app.app_context():
        # Import routes inside to avoid circular imports
        from app.routes.main import main_bp
        from app.routes.ideas import ideas_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(ideas_bp)

        db.create_all()
        ensure_schema_compatibility()

    return app
