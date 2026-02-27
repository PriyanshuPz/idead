from flask import current_app
from sqlalchemy.sql.expression import func
from urllib.parse import urlparse

from app.models import Idea


DIFFICULTY_OPTIONS = {
    1: {
        "value": 1,
        "label": "Conceptual",
        "hint": "Loose framing, early abstraction.",
        "css_class": "difficulty-1",
    },
    2: {
        "value": 2,
        "label": "Weekend Build",
        "hint": "Small and likely shippable quickly.",
        "css_class": "difficulty-2",
    },
    3: {
        "value": 3,
        "label": "Side Project",
        "hint": "Sustained effort over several cycles.",
        "css_class": "difficulty-3",
    },
    4: {
        "value": 4,
        "label": "Deep Build",
        "hint": "Complex architecture and maintenance.",
        "css_class": "difficulty-4",
    },
    5: {
        "value": 5,
        "label": "Obsession Level",
        "hint": "Long-horizon commitment required.",
        "css_class": "difficulty-5",
    },
}


def get_trending_idea():
    return Idea.query.order_by(Idea.upvotes.desc(), Idea.views.desc()).first()


def get_random_idea(exclude_id=None):
    query = Idea.query
    if exclude_id is not None:
        query = query.filter(Idea.id != exclude_id)
    return query.order_by(func.random()).first()


def is_captcha_valid(payload):

    if not current_app.config.get("CAPTCHA_ENABLED", False):
        return True

    # TODO:
    return bool(payload)


def is_likely_url(url):
    if not url:
        return True

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False

    return bool(parsed.netloc)


def get_difficulty_options():
    return [DIFFICULTY_OPTIONS[i] for i in sorted(DIFFICULTY_OPTIONS.keys())]


def get_difficulty_meta(value):
    return DIFFICULTY_OPTIONS.get(int(value or 0), DIFFICULTY_OPTIONS[3])
