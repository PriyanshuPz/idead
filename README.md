**Idead** is a Flask + SQLite web application designed as a resting place for ideas that never made it into reality. It allows people to capture abandoned project ideas, briefly describe what they were about, and note why they were left unfinished.

## Why?

Most people come up with far more ideas than they can realistically build. Over time, these ideas get buried inside notes apps, forgotten drafts, or memory.
Idead exists to give those ideas somewhere to land instead of disappearing unnoticed. 

## How

The application uses:
* Flask application factory + blueprints
* SQLAlchemy ORM with SQLite
* Jinja templates and a restrained cyberpunk-inspired panel UI
* Utility modules for rate limiting, moderation, stats, and idea-selection helpers

With Idead, users can:
* browse the idea graveyard feed
* bury a new idea along with context and reasoning
* open any idea to read its full details
* upvote ideas and report them for moderation
* view dashboard metrics (total ideas, views, burials)

## Run
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

See [TODO.md](./TODO.md) for planned improvements and upcoming ideas.
