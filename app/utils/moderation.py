from flask import current_app
from app.models import db, GlobalStat, Idea


def _increment_burial_count(count: int = 1) -> None:
    stat: GlobalStat | None = GlobalStat.query.first()
    if not stat:
        stat = GlobalStat()
        stat.total_burials = 0
        db.session.add(stat)
    stat.total_burials += count


def check_and_moderate(idea: "Idea") -> bool:
    threshold: int = int(current_app.config.get("REPORT_THRESHOLD", 5))
    if idea.reports >= threshold:
        _increment_burial_count(1)
        db.session.delete(idea)
        db.session.commit()
        return True
    return False


def prune_flagged_ideas() -> int:
    threshold: int = int(current_app.config.get("REPORT_THRESHOLD", 5))

    ideas: list[Idea] = Idea.query.filter(Idea.reports >= threshold).all()
    if not ideas:
        return 0

    for idea in ideas:
        db.session.delete(idea)

    _increment_burial_count(len(ideas))
    db.session.commit()
    return len(ideas)
