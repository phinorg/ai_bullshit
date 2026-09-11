# Agentic Marketing Bullshit Generator

A clone of [dack.com's Web Economy Bullshit Generator](https://www.dack.com/web/bullshit.html),
updated for the agentic marketing era. Click the button, get a phrase:
one verb + one adjective + one noun.

    orchestrate hallucination-free share of model

## Run it

    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5001.

The dev server reads three environment variables:

| variable | default | notes |
| --- | --- | --- |
| `PORT` | `5001` | port to listen on |
| `HOST` | `127.0.0.1` | set to `0.0.0.0` to accept connections from other machines |
| `FLASK_DEBUG` | unset (off) | `1` enables the reloader and the debugger |

    PORT=8000 FLASK_DEBUG=1 python app.py

Leave `FLASK_DEBUG` off whenever `HOST` is not loopback: the Werkzeug
debugger executes arbitrary Python from the browser. For anything beyond
your own machine, use a real WSGI server:

    waitress-serve --host 0.0.0.0 --port 5001 app:app

## Editing the words

Each part of speech lives in its own file, one word per line. Blank lines
and `#` comments are ignored:

    data/verbs.txt
    data/adjectives.txt
    data/nouns.txt

The app re-reads a file whenever its modification time changes, so a save
plus a browser reload is enough — no restart.

## API

`GET /api/phrase` returns the parts and the assembled phrase:

    {"verb": "orchestrate", "adjective": "hallucination-free",
     "noun": "share of model", "phrase": "orchestrate hallucination-free share of model"}
