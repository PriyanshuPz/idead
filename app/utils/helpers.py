from flask import current_app
from sqlalchemy.sql.expression import func

from app.models import Idea


def get_trending_idea():
    """Return the highest-upvoted idea with views as tiebreaker."""
    return Idea.query.order_by(Idea.upvotes.desc(), Idea.views.desc()).first()


def get_random_idea():
    """Return a random idea."""
    return Idea.query.order_by(func.random()).first()


def is_captcha_valid(payload):
    """
    Placeholder for CAPTCHA verification.
    Returns True while CAPTCHA is disabled.
    """
    if not current_app.config.get("CAPTCHA_ENABLED", False):
        return True

    # TODO: validate payload against an external CAPTCHA provider.
    return bool(payload)
