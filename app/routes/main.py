from flask import render_template, request
from app.routes import main_bp
from app.models import Idea
from app.utils.helpers import get_trending_idea, get_random_idea
from app.utils.moderation import prune_flagged_ideas
from app.utils.stats import get_stats


@main_bp.route("/")
def index():
    prune_flagged_ideas()
    stats = get_stats()
    trending_idea = get_trending_idea()
    random_idea = get_random_idea(exclude_id=trending_idea.id if trending_idea else None)
    return render_template(
        "index.html", stats=stats, trending=trending_idea, random=random_idea
    )


@main_bp.route("/yard")
def yard():
    prune_flagged_ideas()
    sort_by = request.args.get("sort", "newest")

    query = Idea.query

    if sort_by == "viewed":
        query = query.order_by(Idea.views.desc())
    elif sort_by == "upvoted":
        query = query.order_by(Idea.upvotes.desc())
    elif sort_by == "lowest_difficulty":
        query = query.order_by(Idea.difficulty.asc(), Idea.created_at.desc())
    else:
        query = query.order_by(Idea.created_at.desc())

    ideas = query.all()
    return render_template("yard.html", ideas=ideas, current_sort=sort_by)


@main_bp.route("/about")
def about():
    return render_template("about.html")
