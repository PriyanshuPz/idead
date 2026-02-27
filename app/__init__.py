from datetime import datetime, timezone
import os

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from app.models import db
from app.utils.helpers import get_difficulty_meta, get_difficulty_options
from app.utils.schema import ensure_schema_compatibility
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    app.config["BUILD_TIMESTAMP"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    @app.context_processor
    def inject_build_metadata():
        return {
            "last_built": app.config.get("BUILD_TIMESTAMP"),
            "difficulty_options": get_difficulty_options(),
            "difficulty_meta": get_difficulty_meta,
        }

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def rate_limited_error(error):
        return render_template("429.html"), 429

    @app.errorhandler(Exception)
    def generic_error(error):
        if isinstance(error, HTTPException):
            return error
        return render_template("error.html"), 500

    with app.app_context():
        from app.routes.main import main_bp
        from app.routes.ideas import ideas_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(ideas_bp)

        db.create_all()
        ensure_schema_compatibility()

    return app
