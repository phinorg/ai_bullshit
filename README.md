# Agentic Marketing Bullshit Generator

A clone of [dack.com's Web Economy Bullshit Generator](https://www.dack.com/web/bullshit.html),
updated for the agentic marketing era. Click the button, get a phrase:
one verb + one adjective + one noun.

    orchestrate hallucination-free share of model

## Run it

    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5001.

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
