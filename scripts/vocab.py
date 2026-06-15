#!/usr/bin/env python3
"""Safe helpers for editing Deutsch Trainer vocabulary JSON files.

Examples:
  python3 scripts/vocab.py check
  python3 scripts/vocab.py add-word --de "der Honig" --ru "мёд" --article der --plural "—" --topic "Essen und Trinken"
  python3 scripts/vocab.py add-words /tmp/new_words.json
  python3 scripts/vocab.py add-verbs /tmp/new_verbs.json
  python3 scripts/vocab.py add-phrases /tmp/new_phrases.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
WORDS = PUBLIC / "words.json"
VERBS = PUBLIC / "verbs.json"
PHRASES = PUBLIC / "phrases.json"

WORD_FIELDS = ["de", "ru", "plural", "article", "topic"]
VERB_FIELDS = ["de", "infinitive", "ru", "cases", "level", "conjugation", "example_de", "example_ru"]
CONJ_FIELDS = ["ich", "du", "er/sie/es", "wir", "ihr", "sie/Sie"]
PHRASE_FIELDS = ["id", "de", "ru", "example_de", "example_ru"]


def load_json(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: {path} is not valid JSON: {exc}") from exc
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise SystemExit(f"ERROR: {path} must contain a JSON array of objects")
    return data


def load_input(path: str) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise SystemExit("ERROR: input must be a JSON object or an array of objects")
    return data


def norm(value: Any) -> str:
    return str(value or "").strip().casefold()


def missing(item: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if field not in item or item[field] in (None, "")]


def validate_word(item: dict[str, Any], *, require_topic: bool = True) -> None:
    fields = WORD_FIELDS if require_topic else ["de", "ru", "plural", "article"]
    required = missing(item, fields)
    if required:
        raise SystemExit(f"ERROR: word {item!r} missing fields: {', '.join(required)}")
    if require_topic and item["article"] not in {"der", "die", "das", "—", "-"}:
        raise SystemExit(f"ERROR: word {item['de']!r} has invalid article {item['article']!r}")


def validate_verb(item: dict[str, Any]) -> None:
    required = missing(item, VERB_FIELDS)
    if required:
        raise SystemExit(f"ERROR: verb {item!r} missing fields: {', '.join(required)}")
    if not isinstance(item["cases"], list):
        raise SystemExit(f"ERROR: verb {item['de']!r} cases must be a list")
    if not isinstance(item["conjugation"], dict):
        raise SystemExit(f"ERROR: verb {item['de']!r} conjugation must be an object")
    conj_missing = missing(item["conjugation"], CONJ_FIELDS)
    if conj_missing:
        raise SystemExit(f"ERROR: verb {item['de']!r} conjugation missing: {', '.join(conj_missing)}")


def validate_phrase(item: dict[str, Any]) -> None:
    required = missing(item, PHRASE_FIELDS)
    if required:
        raise SystemExit(f"ERROR: phrase {item!r} missing fields: {', '.join(required)}")
    if not re.fullmatch(r"[a-z0-9_]+", str(item["id"])):
        raise SystemExit(f"ERROR: phrase id {item['id']!r} must use lowercase latin letters, numbers, underscores")


def assert_no_dupes(label: str, values: list[str]) -> None:
    dupes = [value for value, count in Counter(values).items() if value and count > 1]
    if dupes:
        shown = ", ".join(dupes[:20])
        extra = "..." if len(dupes) > 20 else ""
        raise SystemExit(f"ERROR: duplicate {label}: {shown}{extra}")


def check_all() -> None:
    words = load_json(WORDS)
    verbs = load_json(VERBS)
    phrases = load_json(PHRASES)

    for word in words:
        validate_word(word, require_topic=False)
    for verb in verbs:
        validate_verb(verb)
    for phrase in phrases:
        validate_phrase(phrase)

    assert_no_dupes("word de", [norm(item.get("de")) for item in words])
    assert_no_dupes("verb infinitive", [norm(item.get("infinitive") or item.get("de")) for item in verbs])
    assert_no_dupes("phrase id", [norm(item.get("id")) for item in phrases])
    assert_no_dupes("phrase de", [norm(item.get("de")) for item in phrases])

    print(f"OK: words={len(words)}, verbs={len(verbs)}, phrases={len(phrases)}")


def append_compact_words(items: list[dict[str, Any]]) -> None:
    words = load_json(WORDS)
    existing = {norm(item.get("de")) for item in words}
    to_add: list[dict[str, Any]] = []
    skipped: list[str] = []

    for item in items:
        validate_word(item)
        key = norm(item["de"])
        if key in existing:
            skipped.append(item["de"])
            continue
        existing.add(key)
        to_add.append({field: item[field] for field in WORD_FIELDS})

    if not to_add:
        print(f"No new words. skipped={len(skipped)}")
        return

    text = WORDS.read_text(encoding="utf-8").rstrip()
    if not text.endswith("]"):
        raise SystemExit("ERROR: words.json does not end with ]")
    body = text[:-1].rstrip()
    prefix = "\n" if body.endswith("[") else ",\n"
    appended = ",\n".join(
        "  " + json.dumps(item, ensure_ascii=False, separators=(", ", ": "))
        for item in to_add
    )
    WORDS.write_text(body + prefix + appended + "\n]\n", encoding="utf-8")
    check_all()
    print(f"Added words: {len(to_add)}" + (f"; skipped duplicates: {', '.join(skipped)}" if skipped else ""))


def add_pretty(path: Path, items: list[dict[str, Any]], kind: str) -> None:
    data = load_json(path)
    existing_ids: set[str] = set()
    if kind == "verb":
        validate = validate_verb
        key_name = "infinitive"
        existing = {norm(item.get("infinitive") or item.get("de")) for item in data}
    elif kind == "phrase":
        validate = validate_phrase
        key_name = "de"
        existing = {norm(item.get("de")) for item in data}
        existing_ids = {norm(item.get("id")) for item in data}
    else:
        raise AssertionError(kind)

    to_add: list[dict[str, Any]] = []
    skipped: list[str] = []
    for item in items:
        validate(item)
        key = norm(item.get(key_name))
        if key in existing or (kind == "phrase" and norm(item.get("id")) in existing_ids):
            skipped.append(str(item.get(key_name)))
            continue
        existing.add(key)
        if kind == "phrase":
            existing_ids.add(norm(item.get("id")))
            to_add.append({field: item[field] for field in PHRASE_FIELDS})
        else:
            to_add.append({field: item[field] for field in VERB_FIELDS})

    if not to_add:
        print(f"No new {kind}s. skipped={len(skipped)}")
        return

    data.extend(to_add)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check_all()
    print(f"Added {kind}s: {len(to_add)}" + (f"; skipped duplicates: {', '.join(skipped)}" if skipped else ""))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safely edit Deutsch Trainer vocabulary JSON files")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="validate all vocabulary JSON files and duplicate keys")

    add_word = sub.add_parser("add-word", help="add one word to public/words.json")
    add_word.add_argument("--de", required=True)
    add_word.add_argument("--ru", required=True)
    add_word.add_argument("--article", required=True, choices=["der", "die", "das", "—", "-"])
    add_word.add_argument("--plural", required=True)
    add_word.add_argument("--topic", required=True)

    add_words = sub.add_parser("add-words", help="add words from a JSON object/array")
    add_words.add_argument("file")

    add_verbs = sub.add_parser("add-verbs", help="add verbs from a JSON object/array")
    add_verbs.add_argument("file")

    add_phrases = sub.add_parser("add-phrases", help="add phrases from a JSON object/array")
    add_phrases.add_argument("file")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        check_all()
    elif args.command == "add-word":
        append_compact_words([
            {"de": args.de, "ru": args.ru, "plural": args.plural, "article": args.article, "topic": args.topic}
        ])
    elif args.command == "add-words":
        append_compact_words(load_input(args.file))
    elif args.command == "add-verbs":
        add_pretty(VERBS, load_input(args.file), "verb")
    elif args.command == "add-phrases":
        add_pretty(PHRASES, load_input(args.file), "phrase")
    else:
        raise AssertionError(args.command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
