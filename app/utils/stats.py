from app.models import db, Idea, GlobalStat


def get_stats():
    """Returns total ideas, total views, and total burials (deleted ideas)."""
    total_ideas = Idea.query.count()
    total_views = db.session.query(db.func.sum(Idea.views)).scalar() or 0

    stat = GlobalStat.query.first()
    total_burials = stat.total_burials if stat else 0

    return {
        "total_ideas": total_ideas,
        "total_views": total_views,
        "total_burials": total_burials,
    }
