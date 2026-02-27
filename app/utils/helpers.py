from flask import current_app
from sqlalchemy.sql.expression import func
from urllib.parse import urlparse

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


def is_likely_url(url):
    """Light URL validation for optional external project references."""
    if not url:
        return True

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False

    return bool(parsed.netloc)
