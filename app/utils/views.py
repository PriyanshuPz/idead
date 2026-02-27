import re
from typing import Optional

from app.models import IdeaView, db


VIEWER_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{16,64}$")


def normalize_viewer_id(raw_value: str | None) -> Optional[str]:
    if not raw_value:
        return None

    value: str = raw_value.strip()
    if not VIEWER_ID_PATTERN.match(value):
        return None
    return value


def register_unique_view(idea_id: int, viewer_id: str | None) -> bool:

    if not viewer_id:
        return False

    existing: IdeaView | None = IdeaView.query.filter_by(
        idea_id=idea_id, viewer_id=viewer_id
    ).first()
    if existing:
        return False

    new_view = IdeaView()
    new_view.idea_id = idea_id
    new_view.viewer_id = viewer_id
    db.session.add(new_view)
    db.session.commit()
    return True
