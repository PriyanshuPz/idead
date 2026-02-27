import re

from app.models import IdeaView, db


VIEWER_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{16,64}$")


def normalize_viewer_id(raw_value):
    if not raw_value:
        return None

    value = raw_value.strip()
    if not VIEWER_ID_PATTERN.match(value):
        return None
    return value


def register_unique_view(idea_id, viewer_id):
    """
    Store a view once per (idea, viewer_id).
    Returns True when this is a new view, else False.
    """
    if not viewer_id:
        return False

    existing = IdeaView.query.filter_by(idea_id=idea_id, viewer_id=viewer_id).first()
    if existing:
        return False

    db.session.add(IdeaView(idea_id=idea_id, viewer_id=viewer_id))
    return True
