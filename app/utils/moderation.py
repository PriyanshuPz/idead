from flask import current_app
from app.models import db, GlobalStat


def _increment_burial_count(count=1):
    stat = GlobalStat.query.first()
    if not stat:
        stat = GlobalStat(total_burials=0)
        db.session.add(stat)
    stat.total_burials += count


def check_and_moderate(idea):
    """
    Checks if an idea has reached the report threshold.
    If it has, it deletes the idea from the database.
    Returns True if deleted, False otherwise.
    """
    threshold = current_app.config.get("REPORT_THRESHOLD", 5)
    if idea.reports >= threshold:
        _increment_burial_count(1)
        db.session.delete(idea)
        db.session.commit()
        return True
    return False


def prune_flagged_ideas():
    """
    Delete all ideas at or over threshold and return how many were removed.
    Useful when threshold changes or stale flagged ideas exist.
    """
    threshold = current_app.config.get("REPORT_THRESHOLD", 5)
    from app.models import Idea  # local import to avoid circular imports

    ideas = Idea.query.filter(Idea.reports >= threshold).all()
    if not ideas:
        return 0

    for idea in ideas:
        db.session.delete(idea)

    _increment_burial_count(len(ideas))
    db.session.commit()
    return len(ideas)
