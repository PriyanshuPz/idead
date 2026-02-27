from flask import (
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from app.models import Idea, db
from app.routes import ideas_bp
from app.utils.helpers import is_captcha_valid, is_likely_url
from app.utils.moderation import check_and_moderate
from app.utils.rate_limit import rate_limit
from app.utils.views import normalize_viewer_id, register_unique_view


@ideas_bp.route("/bury", methods=["GET", "POST"])
@rate_limit(
    limit=lambda: current_app.config.get("BURY_RATE_LIMIT", 3),
    per=lambda: current_app.config.get("BURY_RATE_PERIOD", 60),
)
def bury():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        reason = (request.form.get("reason") or "").strip()
        project_url = (request.form.get("project_url") or "").strip()
        difficulty = request.form.get("difficulty", type=int)
        captcha_value = (request.form.get("captcha") or "").strip()

        if not is_captcha_valid(captcha_value):
            flash("CAPTCHA verification failed.", "error")
            return redirect(url_for("ideas.bury"))

        if not all([title, description, reason, difficulty]):
            flash("All fields are required.", "error")
            return redirect(url_for("ideas.bury"))

        if difficulty < 1 or difficulty > 5:
            flash("Difficulty must be between 1 and 5.", "error")
            return redirect(url_for("ideas.bury"))

        if not is_likely_url(project_url):
            flash("Project URL must start with http:// or https://", "error")
            return redirect(url_for("ideas.bury"))

        new_idea = Idea(
            title=title,
            description=description,
            reason=reason,
            project_url=project_url or None,
            difficulty=difficulty,
        )

        db.session.add(new_idea)
        db.session.commit()

        flash("Idea buried successfully.", "success")
        return redirect(url_for("main.yard"))

    return render_template(
        "bury.html", captcha_enabled=current_app.config.get("CAPTCHA_ENABLED", False)
    )


@ideas_bp.route("/idea/<int:id>")
def view_idea(id):
    idea = Idea.query.get_or_404(id)

    if check_and_moderate(idea):
        return render_template("idea_not_found.html"), 404

    return render_template("idea.html", idea=idea)


@ideas_bp.route("/idea/<int:id>/view", methods=["POST"])
@rate_limit(
    limit=lambda: current_app.config.get("VIEW_RATE_LIMIT", 30),
    per=lambda: current_app.config.get("VIEW_RATE_PERIOD", 60),
)
def track_view(id):
    idea = Idea.query.get_or_404(id)
    if check_and_moderate(idea):
        return jsonify({"success": False, "message": "Idea no longer exists."}), 404

    payload = request.get_json(silent=True) or {}
    raw_viewer_id = request.headers.get("X-Idead-Viewer", "") or payload.get(
        "viewer_id", ""
    )
    viewer_id = normalize_viewer_id(raw_viewer_id)
    if not viewer_id:
        return jsonify({"success": False, "message": "Invalid viewer token."}), 400

    is_new_view = register_unique_view(id, viewer_id)
    if is_new_view:
        idea.views += 1

    db.session.commit()
    return jsonify({"success": True, "views": idea.views, "counted": is_new_view})


@ideas_bp.route("/idea/<int:id>/upvote", methods=["POST"])
@rate_limit(
    limit=lambda: current_app.config.get("ACTION_RATE_LIMIT", 5),
    per=lambda: current_app.config.get("ACTION_RATE_PERIOD", 60),
)
def upvote(id):
    idea = Idea.query.get_or_404(id)
    if check_and_moderate(idea):
        return jsonify({"success": False, "message": "Idea no longer exists."}), 404

    idea.upvotes += 1
    db.session.commit()

    return jsonify({"success": True, "upvotes": idea.upvotes})


@ideas_bp.route("/idea/<int:id>/report", methods=["POST"])
@rate_limit(
    limit=lambda: current_app.config.get("ACTION_RATE_LIMIT", 5),
    per=lambda: current_app.config.get("ACTION_RATE_PERIOD", 60),
)
def report(id):
    idea = Idea.query.get_or_404(id)
    idea.reports += 1
    db.session.commit()

    deleted = check_and_moderate(idea)

    if deleted:
        return jsonify(
            {"success": True, "deleted": True, "message": "Idea has been buried."}
        )

    return jsonify({"success": True, "deleted": False})
