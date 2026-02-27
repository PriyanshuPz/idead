from sqlalchemy import inspect, text

from app.models import db


def ensure_schema_compatibility():
    """
    Apply tiny, safe schema updates for local SQLite databases
    when running without a migration framework.
    """
    inspector = inspect(db.engine)
    if "ideas" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("ideas")}
    if "project_url" not in existing_columns:
        db.session.execute(text("ALTER TABLE ideas ADD COLUMN project_url VARCHAR(512)"))
        db.session.commit()
