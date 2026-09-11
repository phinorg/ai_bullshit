"""Agentic Marketing Bullshit Generator.

A tribute to dack.com's Web Economy Bullshit Generator, updated for the
era of agents, evals and answer engines. A phrase is one verb, one
adjective and one noun, each drawn from its own file in data/.
"""

import os
import random
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"
LISTS = {"verb": "verbs.txt", "adjective": "adjectives.txt", "noun": "nouns.txt"}

_cache: dict[str, tuple[float, list[str]]] = {}


def load_words(kind: str) -> list[str]:
    """Read one word list, skipping blank lines and # comments.

    Cached until the file changes, so editing data/*.txt takes effect
    without restarting the server.
    """
    path = DATA_DIR / LISTS[kind]
    mtime = path.stat().st_mtime
    cached = _cache.get(kind)
    if cached is None or cached[0] != mtime:
        words = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        if not words:
            raise ValueError(f"{path} has no words in it")
        _cache[kind] = (mtime, words)
    return _cache[kind][1]


def make_phrase() -> dict[str, str]:
    parts = {kind: random.choice(load_words(kind)) for kind in LISTS}
    parts["phrase"] = f"{parts['verb']} {parts['adjective']} {parts['noun']}"
    return parts


@app.route("/")
def index():
    return render_template(
        "index.html",
        first=make_phrase(),
        verbs=load_words("verb"),
        adjectives=load_words("adjective"),
        nouns=load_words("noun"),
    )


@app.route("/api/phrase")
def api_phrase():
    return jsonify(make_phrase())


if __name__ == "__main__":
    # Debug off unless asked for: the Werkzeug debugger runs arbitrary code
    # from the browser, which is a hole as soon as HOST is not loopback.
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5001)),
    )
