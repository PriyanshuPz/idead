from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()


class Idea(db.Model):
    __tablename__ = "ideas"
    __table_args__ = (CheckConstraint("difficulty >= 1 AND difficulty <= 5"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    project_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reports: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class GlobalStat(db.Model):
    __tablename__ = "global_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_burials: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class IdeaView(db.Model):
    __tablename__ = "idea_views"
    __table_args__ = (UniqueConstraint("idea_id", "viewer_id", name="uq_idea_view"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    idea_id: Mapped[int] = mapped_column(ForeignKey("ideas.id"), nullable=False, index=True)
    viewer_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
