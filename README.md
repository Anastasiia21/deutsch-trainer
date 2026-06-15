# Deutsch Trainer

React + Vite app for practicing German vocabulary, verbs, and phrases.

## Project structure

```text
public/
  words.json      # word cards
  verbs.json      # verb cards with conjugation and examples
  phrases.json    # phrase cards with examples
  favicon.svg

src/
  App.jsx         # main trainer UI
  index.css       # styles
  main.jsx        # app entry point

scripts/
  vocab.py        # helper for safe vocabulary edits

.github/workflows/
  hourly-add-word.yml
```

## Main commands

Install dependencies:

```bash
npm install
```

Run locally:

```bash
npm run dev
```

Build production version:

```bash
npm run build
```

Check vocabulary JSON files:

```bash
npm run vocab:check
```

## Vocabulary files

### Words

File:

```text
public/words.json
```

Typical card:

```json
{
  "de": "der Honig",
  "ru": "мёд",
  "plural": "—",
  "article": "der",
  "topic": "Essen und Trinken"
}
```

Words are shown German-first. The back side shows Russian and plural when available.

### Verbs

File:

```text
public/verbs.json
```

Typical card:

```json
{
  "de": "einschlafen",
  "infinitive": "einschlafen",
  "ru": "засыпать",
  "cases": ["Nominativ"],
  "level": "A1",
  "conjugation": {
    "ich": "schlafe ein",
    "du": "schläfst ein",
    "er/sie/es": "schläft ein",
    "wir": "schlafen ein",
    "ihr": "schlaft ein",
    "sie/Sie": "schlafen ein"
  },
  "example_de": "Ich schlafe schnell ein.",
  "example_ru": "Я быстро засыпаю."
}
```

### Phrases

File:

```text
public/phrases.json
```

Typical card:

```json
{
  "id": "das_verstehe_ich_nicht",
  "de": "Das verstehe ich nicht.",
  "ru": "Я этого не понимаю.",
  "example_de": "Entschuldigung, das verstehe ich nicht.",
  "example_ru": "Извините, я этого не понимаю."
}
```

Phrase cards are shown German-first. After flip, the Russian translation and examples are shown.

## Safe vocabulary editing

Use the helper script instead of manually editing large JSON files.

### Check all vocabulary files

```bash
npm run vocab:check
```

This validates JSON and checks duplicates:

- words: by `de`
- verbs: by `infinitive`
- phrases: by `id` and `de`

### Add one word

```bash
python3 scripts/vocab.py add-word \
  --de "der Honig" \
  --ru "мёд" \
  --article der \
  --plural "—" \
  --topic "Essen und Trinken"
```

### Add many words

Create a temporary JSON file:

```json
[
  {
    "de": "der Senf",
    "ru": "горчица",
    "plural": "—",
    "article": "der",
    "topic": "Essen und Trinken"
  }
]
```

Then run:

```bash
python3 scripts/vocab.py add-words /tmp/new_words.json
```

### Add verbs

```bash
python3 scripts/vocab.py add-verbs /tmp/new_verbs.json
```

### Add phrases

```bash
python3 scripts/vocab.py add-phrases /tmp/new_phrases.json
```

## Editing rules

Before committing:

```bash
npm run vocab:check
git diff --check
npm run build
```

When adding vocabulary:

- do not add duplicates
- prefer everyday/common words
- put food words under `Essen und Trinken`
- put paired/opposite words under `Парные слова`
- keep `words.json` compact, one object per line
- use `—` for missing plural instead of an empty string

## Automation

The workflow:

```text
.github/workflows/hourly-add-word.yml
```

runs:

```bash
python hourly_add_word.py
```

It can update:

```text
public/verbs.json
new_verbs.txt
```

Related files:

```text
hourly_add_word.py
import_new_verbs.py
new_verbs.txt
```

Do not delete these unless the automation is intentionally removed.

## Git workflow

Recommended flow:

```bash
git status --short --branch
npm run vocab:check
npm run build
git add <changed files>
git commit -m "Short description"
git push
```
